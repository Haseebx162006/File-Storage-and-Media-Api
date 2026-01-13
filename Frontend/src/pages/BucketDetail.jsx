import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import {
    ArrowLeft, Upload, File as FileIcon, Trash2, Download, Search, MoveRight
} from 'lucide-react';
import toast from 'react-hot-toast';

const formatBytes = (bytes, decimals = 2) => {
    if (!+bytes) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
};

const BucketDetail = () => {
    const { bucketId } = useParams();
    const navigate = useNavigate();
    const [bucket, setBucket] = useState(null);
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const fileInputRef = useRef(null);

    const fetchBucketDetails = async () => {
        try {
            const bucketRes = await api.get(`/api/buckets/${bucketId}`);
            setBucket(bucketRes.data);
            const filesRes = await api.get(`/api/buckets/${bucketId}/files`);
            setFiles(filesRes.data);
        } catch (error) {
            console.error(error);
            toast.error('Failed to load details');
            navigate('/dashboard');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (bucketId) {
            fetchBucketDetails();
        }
    }, [bucketId]);

    const handleFileUpload = async (e) => {
        const selectedFiles = Array.from(e.target.files);
        if (selectedFiles.length === 0) return;

        // Validate file sizes (Vercel limit: 4.5MB, we use 4MB to be safe)
        const MAX_FILE_SIZE = 4 * 1024 * 1024; // 4MB
        const oversizedFiles = selectedFiles.filter(f => f.size > MAX_FILE_SIZE);

        if (oversizedFiles.length > 0) {
            toast.error(
                `File(s) too large: ${oversizedFiles.map(f => f.name).join(', ')}. Max size: 4MB per file.`
            );
            if (fileInputRef.current) fileInputRef.current.value = '';
            return;
        }

        setUploading(true);
        const toastId = toast.loading('Uploading files...');

        try {
            for (const file of selectedFiles) {
                const formData = new FormData();
                formData.append('file', file);
                await api.post(`/api/buckets/${bucketId}/files`, formData, {
                    headers: { 'Content-Type': 'multipart/form-data' },
                    maxBodyLength: Infinity,
                    maxContentLength: Infinity
                });
            }
            toast.success('Files uploaded', { id: toastId });
            fetchBucketDetails();
        } catch (error) {
            console.error('Upload error:', error);
            const errorMsg = error.response?.data?.detail || error.response?.statusText || 'Upload failed';
            toast.error(errorMsg, { id: toastId });
        } finally {
            setUploading(false);
            if (fileInputRef.current) fileInputRef.current.value = '';
        }
    };

    const handleDeleteFile = async (fileId) => {
        if (!window.confirm("Permanently delete this file?")) return;
        try {
            await api.delete(`/api/files/${fileId}`);
            toast.success("File deleted");
            setFiles(files.filter(f => f.id !== fileId));
        } catch (error) {
            toast.error("Failed to delete file");
        }
    };

    const handleMoveFile = async (fileId) => {
        const targetBucketId = window.prompt('Enter target bucket ID:', '');
        if (!targetBucketId) return;

        try {
            await api.patch(`/api/files/${fileId}/move/${targetBucketId}`);
            toast.success('File moved');
            fetchBucketDetails();
        } catch (error) {
            console.error(error);
            toast.error(error.response?.data?.detail || 'Failed to move file');
        }
    };

    const handleDownloadFile = async (fileId, fileName) => {
        try {
            const response = await api.get(`/api/files/${fileId}/download`, {
                responseType: 'blob'
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', fileName);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            toast.error("Download failed");
        }
    };

    const filteredFiles = files.filter(f =>
        f.file_name?.toLowerCase().includes(searchQuery.toLowerCase())
    );

    if (loading) {
        return (
            <div className="flex h-[50vh] items-center justify-center">
                <div className="h-8 w-8 animate-spin rounded-full border-2 border-slate-200 border-t-slate-900" />
            </div>
        );
    }

    if (!bucket) return null;

    return (
        <div className="space-y-6">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-zinc-200 pb-5">
                <div className="flex items-center gap-4">
                    <Button variant="secondary" size="icon" onClick={() => navigate('/dashboard')} className="shrink-0 h-9 w-9">
                        <ArrowLeft className="h-4 w-4" />
                    </Button>
                    <div>
                        <h1 className="text-xl font-bold text-black">{bucket.name}</h1>
                        <div className="flex items-center gap-2 text-sm text-zinc-500 mt-1">
                            <span className="bg-zinc-100 px-2 py-0.5 rounded text-xs font-medium border border-zinc-200">ID: {bucket.id}</span>
                            <span>•</span>
                            <span>{files.length} items</span>
                            <span>•</span>
                            <span>{formatBytes(files.reduce((acc, curr) => acc + (curr.file_size || 0), 0))} used</span>
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-3 w-full sm:w-auto">
                    <div className="relative flex-1 sm:w-64">
                        <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-400" />
                        <Input
                            className="pl-9 bg-white border-zinc-200 focus:ring-black"
                            placeholder="Filter files..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>
                    <div className="relative">
                        <input
                            type="file"
                            multiple
                            className="hidden"
                            ref={fileInputRef}
                            onChange={handleFileUpload}
                        />
                        <Button onClick={() => fileInputRef.current?.click()} isLoading={uploading}>
                            <Upload className="mr-2 h-4 w-4" />
                            Upload
                        </Button>
                    </div>
                </div>
            </div>

            <Card className="overflow-hidden border-zinc-200 shadow-sm">
                <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left">
                        <thead className="bg-zinc-50 text-zinc-600 font-medium border-b border-zinc-200">
                            <tr>
                                <th className="px-6 py-3 w-[40%]">Name</th>
                                <th className="px-6 py-3 w-[15%]">Size</th>
                                <th className="px-6 py-3 w-[20%]">Uploaded</th>
                                <th className="px-6 py-3 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-zinc-100 bg-white">
                            {filteredFiles.length === 0 ? (
                                <tr>
                                    <td colSpan="4" className="px-6 py-24 text-center">
                                        <div className="flex flex-col items-center justify-center">
                                            <div className="h-10 w-10 bg-zinc-50 rounded-full flex items-center justify-center mb-3">
                                                <FileIcon className="h-5 w-5 text-zinc-400" />
                                            </div>
                                            <p className="text-black font-medium">No files found</p>
                                            <p className="text-zinc-500 text-xs">Upload files to get started</p>
                                        </div>
                                    </td>
                                </tr>
                            ) : (
                                filteredFiles.map((file) => (
                                    <tr key={file.id} className="hover:bg-zinc-50/80 group transition-colors">
                                        <td className="px-6 py-3">
                                            <div className="flex items-center gap-3">
                                                <FileIcon className="h-4 w-4 text-zinc-400 shrink-0" />
                                                <span className="font-medium text-zinc-800 truncate max-w-xs">{file.file_name}</span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-3 text-zinc-500 font-mono text-xs">{formatBytes(file.file_size)}</td>
                                        <td className="px-6 py-3 text-zinc-500">
                                            {new Date(file.created_at).toLocaleDateString()}
                                        </td>
                                        <td className="px-6 py-3 text-right">
                                            <div className="flex items-center justify-end gap-1 opacity-100 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity">
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    className="h-8 w-8 text-zinc-400 hover:text-black"
                                                    onClick={() => handleMoveFile(file.id)}
                                                    title="Move"
                                                >
                                                    <MoveRight className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    className="h-8 w-8 text-zinc-400 hover:text-black"
                                                    onClick={() => handleDownloadFile(file.id, file.file_name)}
                                                    title="Download"
                                                >
                                                    <Download className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    className="h-8 w-8 text-zinc-400 hover:text-red-600"
                                                    onClick={() => handleDeleteFile(file.id)}
                                                    title="Delete"
                                                >
                                                    <Trash2 className="h-4 w-4" />
                                                </Button>
                                            </div>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </Card>
        </div>
    );
};

export default BucketDetail;
