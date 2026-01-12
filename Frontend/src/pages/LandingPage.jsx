import { Link } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Cloud, Shield, Share2, Zap, LayoutGrid, HardDrive, Check } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const LandingPage = () => {
    const { user } = useAuth();

    return (
        <div className="bg-white min-h-screen font-sans selection:bg-black selection:text-white">
            <header className="absolute inset-x-0 top-0 z-50">
                <nav className="flex items-center justify-between p-6 lg:px-8 border-b border-zinc-100 bg-white/80 backdrop-blur-md" aria-label="Global">
                    <div className="flex lg:flex-1">
                        <Link to="/" className="-m-1.5 p-1.5 flex items-center space-x-3 group">
                            <div className="h-8 w-8 bg-black rounded-lg flex items-center justify-center transition-transform group-hover:scale-105 group-hover:rotate-3">
                                <span className="text-white font-bold text-lg">H</span>
                            </div>
                            <span className="font-bold text-xl text-black tracking-tight">H-Cloud</span>
                        </Link>
                    </div>
                    <div className="flex items-center gap-x-6">
                        {user ? (
                            <Link to="/dashboard" className="text-sm font-semibold leading-6 text-black hover:text-zinc-600 transition-colors">
                                Dashboard <span aria-hidden="true">&rarr;</span>
                            </Link>
                        ) : (
                            <Link to="/login" className="text-sm font-bold leading-6 text-black hover:text-zinc-600 transition-colors">
                                Log in <span aria-hidden="true">&rarr;</span>
                            </Link>
                        )}
                    </div>
                </nav>
            </header>

            <div className="relative isolate px-6 pt-14 lg:px-8">
                <div className="mx-auto max-w-7xl py-16 sm:py-20 lg:py-24">
                    <div className="text-center">
                        {/* Decorative Dice Element */}
                        <div className="flex justify-center mb-6">
                            <div className="relative">
                                <div className="h-16 w-16 bg-black rounded-2xl rotate-12 shadow-2xl flex items-center justify-center transform hover:rotate-0 transition-transform duration-500">
                                    <div className="grid grid-cols-2 gap-1.5 p-2">
                                        <div className="h-2 w-2 bg-white rounded-full"></div>
                                        <div className="h-2 w-2 bg-white rounded-full"></div>
                                        <div className="h-2 w-2 bg-white rounded-full"></div>
                                        <div className="h-2 w-2 bg-white rounded-full"></div>
                                    </div>
                                </div>
                                <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 h-1.5 w-12 bg-zinc-200 rounded-full blur-sm"></div>
                            </div>
                        </div>

                        <h1 className="text-5xl font-extrabold tracking-tight text-black sm:text-7xl mb-8">
                            Gravity defying <br />
                            <span className="text-zinc-500">storage solutions.</span>
                        </h1>
                        <p className="mt-4 text-lg leading-8 text-zinc-600 max-w-2xl mx-auto">
                            Minimal, powerful, and secure. H-Cloud brings you the future of object storage with zero friction.
                        </p>
                        <div className="mt-8 flex items-center justify-center gap-x-4">
                            {user ? (
                                <Link to="/dashboard">
                                    <Button size="lg" className="px-10 h-12 text-lg bg-black text-white hover:bg-zinc-800 rounded-full border border-black transition-all hover:px-12">
                                        Enter Console
                                    </Button>
                                </Link>
                            ) : (
                                <Link to="/signup">
                                    <Button size="lg" className="px-10 h-12 text-lg bg-black text-white hover:bg-zinc-800 rounded-full border border-black transition-all hover:px-12">
                                        Start Free
                                    </Button>
                                </Link>
                            )}
                        </div>
                    </div>

                    {/* Key Benefits - Compact Grid */}
                    <div className="mt-10 sm:mt-12">
                        <div className="grid grid-cols-3 gap-3 max-w-3xl mx-auto">
                            <div className="bg-white border border-zinc-200 rounded-lg p-4 text-center hover:border-black transition-colors">
                                <div className="h-10 w-10 bg-black rounded-lg flex items-center justify-center mx-auto mb-2">
                                    <HardDrive className="h-5 w-5 text-white" />
                                </div>
                                <div className="text-xs font-bold text-black">500MB Free</div>
                                <div className="text-xs text-zinc-500 mt-0.5">Per bucket</div>
                            </div>
                            <div className="bg-white border border-zinc-200 rounded-lg p-4 text-center hover:border-black transition-colors">
                                <div className="h-10 w-10 bg-black rounded-lg flex items-center justify-center mx-auto mb-2">
                                    <Shield className="h-5 w-5 text-white" />
                                </div>
                                <div className="text-xs font-bold text-black">Private</div>
                                <div className="text-xs text-zinc-500 mt-0.5">By default</div>
                            </div>
                            <div className="bg-white border border-zinc-200 rounded-lg p-4 text-center hover:border-black transition-colors">
                                <div className="h-10 w-10 bg-black rounded-lg flex items-center justify-center mx-auto mb-2">
                                    <Zap className="h-5 w-5 text-white" />
                                </div>
                                <div className="text-xs font-bold text-black">Fast</div>
                                <div className="text-xs text-zinc-500 mt-0.5">Global CDN</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Features Section */}
            <div className="py-16 sm:py-20 bg-zinc-50">
                <div className="mx-auto max-w-7xl px-6 lg:px-8">
                    <div className="mx-auto max-w-2xl text-center mb-12">
                        <h2 className="text-3xl font-bold tracking-tight text-black sm:text-4xl">Everything you need</h2>
                        <p className="mt-3 text-lg text-zinc-600">Simple, powerful features designed for modern teams.</p>
                    </div>
                    <div className="mx-auto grid max-w-2xl grid-cols-1 gap-6 sm:grid-cols-2 lg:mx-0 lg:max-w-none lg:grid-cols-3">
                        {features.map((feature) => (
                            <div key={feature.name} className="bg-white rounded-xl p-6 border border-zinc-200 hover:border-black transition-colors">
                                <div className="h-12 w-12 bg-black rounded-lg flex items-center justify-center mb-4">
                                    <feature.icon className="h-6 w-6 text-white" />
                                </div>
                                <h3 className="text-lg font-bold text-black mb-2">{feature.name}</h3>
                                <p className="text-sm text-zinc-600 leading-relaxed">{feature.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Stats Section */}
            <div className="py-16 sm:py-20">
                <div className="mx-auto max-w-7xl px-6 lg:px-8">
                    <div className="mx-auto max-w-2xl lg:max-w-none">
                        <div className="grid grid-cols-1 gap-8 sm:grid-cols-3">
                            <div className="text-center">
                                <div className="text-4xl font-bold tracking-tight text-black">99.9%</div>
                                <div className="mt-2 text-sm text-zinc-600">Uptime guarantee</div>
                            </div>
                            <div className="text-center">
                                <div className="text-4xl font-bold tracking-tight text-black">500MB</div>
                                <div className="mt-2 text-sm text-zinc-600">Free storage per bucket</div>
                            </div>
                            <div className="text-center">
                                <div className="text-4xl font-bold tracking-tight text-black">Lightning</div>
                                <div className="mt-2 text-sm text-zinc-600">Fast global delivery</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="border-t border-zinc-100 py-8">
                <div className="mx-auto max-w-7xl px-6 lg:px-8 flex justify-between items-center text-zinc-400 text-sm">
                    <p>&copy; 2026 H-Cloud Inc.</p>
                    <div className="flex gap-4">
                        <a href="#" className="hover:text-black">Privacy</a>
                        <a href="#" className="hover:text-black">Terms</a>
                    </div>
                </div>
            </div>
        </div>
    );
};

const features = [
    {
        name: 'Bucket Storage',
        description: 'Create distinct buckets to organize your digital assets. Set custom storage limits for better control.',
        icon: HardDrive,
    },
    {
        name: 'Secure by Default',
        description: 'Enterprise-grade encryption and access controls ensure your data remains private and secure.',
        icon: Shield,
    },
    {
        name: 'Lightning Fast',
        description: 'Edge-cached delivery ensures your users get their content with minimal latency.',
        icon: Zap,
    },
];

export default LandingPage;
