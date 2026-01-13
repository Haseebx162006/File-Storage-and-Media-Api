import { useState, useEffect } from 'react';
import api from '../services/api';
import { Button } from '../components/ui/Button';
import { Card, CardContent } from '../components/ui/Card';
import CreateBucketModal from '../components/Modals/CreateBucketModal';
import { Plus, Trash2, HardDrive, Search, MoreHorizontal } from 'lucide-react';
import toast from 'react-hot-toast';
import { Link } from 'react-router-dom';
import { cn } from '../utils';

const Dashboard = () => {
    const [buckets, setBuckets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const fetchBuckets = async () => {
        try {
            const response = await api.get('/api/buckets');
            setBuckets(response.data);
        } catch (error) {
            console.error(error);
            toast.error('Failed to load buckets');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchBuckets();
    }, []);

    const handleDeleteBucket = async (e, id) => {
        e.preventDefault();
        e.stopPropagation();
        if (!window.confirm('Are you sure you want to delete this bucket?')) return;

        try {
            await api.delete(`/api/buckets/${id}`);
            toast.success('Bucket deleted');
            setBuckets(buckets.filter(b => b.id !== id));
        } catch (error) {
            console.error(error);
            const message = error.response?.data?.detail || 'Failed to delete bucket';
            toast.error(message);
        }
    };

    if (loading) {
        return (
            <div className="flex h-[50vh] items-center justify-center">
                <div className="h-8 w-8 animate-spin rounded-full border-2 border-slate-200 border-t-slate-900" />
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-zinc-200 pb-5">
                <div>
                    <h1 className="text-2xl font-bold tracking-tight text-black">Buckets</h1>
                    <p className="text-sm text-zinc-500 mt-1">Manage your object storage containers with zero gravity.</p>
                </div>
                <Button onClick={() => setIsModalOpen(true)} className="bg-black text-white hover:bg-zinc-800">
                    <Plus className="mr-2 h-4 w-4" />
                    Create Bucket
                </Button>
            </div>

            {buckets.length === 0 ? (
                <div className="rounded-2xl border border-dashed border-zinc-300 p-12 text-center bg-zinc-50/50 hover:bg-zinc-50 transition-colors">
                    <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-white border border-zinc-200 shadow-sm">
                        <HardDrive className="h-6 w-6 text-zinc-400" />
                    </div>
                    <h3 className="mt-4 text-sm font-bold text-black">No buckets created</h3>
                    <p className="mt-1 text-sm text-zinc-500">Get started by creating a new storage bucket.</p>
                    <div className="mt-6">
                        <Button onClick={() => setIsModalOpen(true)} className="bg-black text-white hover:bg-zinc-800">
                            Create Bucket
                        </Button>
                    </div>
                </div>
            ) : (
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                    {buckets.map((bucket) => (
                        <Link key={bucket.id} to={`/api/buckets/${bucket.id}`} className="group block focus:outline-none">
                            <Card className="h-full transition-all hover:shadow-lg hover:-translate-y-1 hover:border-black/20 duration-300">
                                <CardContent className="p-6">
                                    <div className="flex items-start justify-between">
                                        <div className="flex items-center gap-4">
                                            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-zinc-50 border border-zinc-100 group-hover:bg-black group-hover:text-white transition-colors duration-300">
                                                <HardDrive className="h-6 w-6 transition-colors" />
                                            </div>
                                            <div>
                                                <h3 className="font-bold text-lg text-black">{bucket.name}</h3>
                                                <p className="text-xs text-zinc-500 font-mono">
                                                    {new Date(bucket.created_at).toLocaleDateString()}
                                                </p>
                                            </div>
                                        </div>
                                        <button
                                            onClick={(e) => handleDeleteBucket(e, bucket.id)}
                                            className="rounded-full p-2 text-zinc-300 hover:text-red-600 hover:bg-red-50 focus:outline-none opacity-0 group-hover:opacity-100 transition-all"
                                            title="Delete Bucket"
                                        >
                                            <Trash2 className="h-4 w-4" />
                                        </button>
                                    </div>

                                    <div className="mt-8">
                                        <div className="mb-2 flex items-center justify-between text-xs">
                                            <span className="text-zinc-500 font-medium">USAGE</span>
                                            <span className="font-bold text-black font-mono">
                                                {bucket.used_Storage ? (bucket.used_Storage / (1024 * 1024)).toFixed(2) + ' MB' : '0 MB'}
                                            </span>
                                        </div>
                                        <div className="h-2 w-full overflow-hidden rounded-full bg-zinc-100">
                                            <div
                                                className="h-full rounded-full bg-black"
                                                style={{ width: `${Math.min(((bucket.used_Storage || 0) / (bucket.storage_limit || 524288000)) * 100, 100)}%` }}
                                            />
                                        </div>
                                        <div className="mt-2 text-xs text-zinc-400 text-right font-mono">
                                            / {(bucket.storage_limit ? bucket.storage_limit : 524288000) / (1024 * 1024)} MB
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        </Link>
                    ))}
                </div>
            )}

            <CreateBucketModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onBucketCreated={fetchBuckets}
            />
        </div>
    );
};

export default Dashboard;
