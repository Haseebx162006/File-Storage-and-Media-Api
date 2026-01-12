import { useState } from 'react';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import toast from 'react-hot-toast';
import api from '../../services/api';
import { X } from 'lucide-react';

export default function CreateBucketModal({ isOpen, onClose, onBucketCreated }) {
    const [name, setName] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!name.trim()) return;

        setLoading(true);
        try {
            const payload = { name, is_public: false, storage_limit: 524288000 }; // 500MB default
            await api.post('/buckets', payload);
            toast.success('Bucket created successfully');
            setName('');
            onBucketCreated();
            onClose();
        } catch (error) {
            console.error(error);
            toast.error(error.response?.data?.detail || 'Failed to create bucket');
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-zinc-900/40 backdrop-blur-sm animate-in fade-in duration-200">
            <div className="bg-white rounded-lg shadow-xl w-full max-w-md overflow-hidden animate-in zoom-in-95 duration-200 border border-zinc-200">
                <div className="flex items-center justify-between p-5 border-b border-zinc-100">
                    <div>
                        <h2 className="text-lg font-bold text-black">New Bucket</h2>
                        <p className="text-sm text-zinc-500">Create a container for your files</p>
                    </div>
                    <button onClick={onClose} className="text-zinc-400 hover:text-black transition-colors">
                        <X className="h-5 w-5" />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="p-5 space-y-4">
                    <Input
                        label="Bucket Name"
                        placeholder="e.g., project-assets"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        autoFocus
                        required
                        className="bg-white"
                    />

                    <div className="flex flex-col gap-2">
                        <div className="text-xs text-zinc-500 bg-zinc-50 p-3 rounded-md border border-zinc-200">
                            <span className="font-bold text-black block mb-1">Bucket configuration:</span>
                            • Private access by default<br />
                            • 500MB storage limit<br />
                            • Standard performance class
                        </div>
                    </div>

                    <div className="flex justify-end space-x-3 pt-4 border-t border-zinc-50 mt-4">
                        <Button type="button" variant="secondary" onClick={onClose}>
                            Cancel
                        </Button>
                        <Button type="submit" isLoading={loading}>
                            Create Bucket
                        </Button>
                    </div>
                </form>
            </div>
        </div>
    );
}
