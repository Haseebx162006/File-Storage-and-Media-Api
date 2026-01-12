import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Card, CardContent } from '../components/ui/Card';
import toast from 'react-hot-toast';

const Signup = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const { signup } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await signup(name, email, password);
            toast.success('Account created! Please log in.');
            navigate('/login');
        } catch (error) {
            console.error(error);
            toast.error(error.response?.data?.detail || 'Failed to create account');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-white px-4 selection:bg-black selection:text-white">
            <div className="mb-8 text-center">
                <div className="h-12 w-12 bg-black rounded-xl flex items-center justify-center mx-auto mb-4 shadow-xl">
                    <span className="text-white font-bold text-2xl">H</span>
                </div>
                <h2 className="text-3xl font-extrabold tracking-tight text-black">Join H-Cloud</h2>
                <p className="text-zinc-500 mt-2 font-medium">Create your secure storage account</p>
            </div>

            <Card className="w-full max-w-sm shadow-2xl border-zinc-100 bg-white">
                <CardContent className="pt-8 px-8 pb-8">
                    <form onSubmit={handleSubmit} className="space-y-5">
                        <Input
                            label="Full Name"
                            type="text"
                            placeholder="John Doe"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                        <Input
                            label="Email"
                            type="email"
                            placeholder="name@example.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                        <Input
                            label="Password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            minLength={6}
                        />
                        <Button type="submit" className="w-full" isLoading={loading}>
                            Create Account
                        </Button>
                    </form>
                    <div className="mt-8 text-center text-sm text-zinc-500">
                        Already have an account?{' '}
                        <Link to="/login" className="text-black font-bold hover:underline underline-offset-4">
                            Log in
                        </Link>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};

export default Signup;
