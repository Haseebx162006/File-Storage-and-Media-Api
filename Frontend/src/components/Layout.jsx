import { useNavigate, useLocation, Link, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from './ui/Button';
import { LogOut, LayoutGrid, HardDrive, User, Menu, X, ChevronRight } from 'lucide-react';
import { useState } from 'react';
import { cn } from '../utils';

const Layout = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [userEmail, setUserEmail] = useState('');

    useState(() => {
        // Get email from localStorage if not in user object
        if (!user?.email) {
            const email = localStorage.getItem('user_email');
            setUserEmail(email || '');
        } else {
            setUserEmail(user.email);
        }
    }, [user]);

    const navItems = [
        { name: 'Buckets', icon: LayoutGrid, path: '/dashboard' },
        // { name: 'Settings', icon: User, path: '/settings' },
    ];

    return (
        <div className="flex h-screen bg-slate-50">
            {/* Sidebar for Desktop */}
            <aside className="hidden md:flex w-64 flex-col border-r border-zinc-200 bg-white">
                <div className="flex h-16 items-center px-6 border-b border-zinc-100">
                    <div className="flex items-center space-x-3">
                        <div className="h-8 w-8 bg-black rounded-lg flex items-center justify-center shadow-sm">
                            <span className="text-white text-lg font-bold">H</span>
                        </div>
                        <span className="text-lg font-bold text-black tracking-tight">
                            H-Cloud
                        </span>
                    </div>
                </div>

                <nav className="flex-1 space-y-1 p-4">
                    {navItems.map((item) => {
                        const Icon = item.icon;
                        const isActive = location.pathname === item.path;

                        return (
                            <Link
                                key={item.path}
                                to={item.path}
                                className={cn(
                                    "flex items-center space-x-3 text-sm font-medium rounded-md px-3 py-2 transition-colors",
                                    isActive
                                        ? "bg-black text-white"
                                        : "text-zinc-600 hover:bg-zinc-100 hover:text-black"
                                )}
                            >
                                <Icon className={cn("h-5 w-5", isActive ? "text-white" : "text-zinc-400")} />
                                <span>{item.name}</span>
                                {isActive && <ChevronRight className="ml-auto h-4 w-4 text-zinc-400" />}
                            </Link>
                        );
                    })}
                </nav>

                <div className="p-4 border-t border-slate-100">
                    <div className="flex items-center space-x-3 mb-4 px-2">
                        <div className="h-8 w-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 font-bold border border-slate-200">
                            {user?.name?.[0]?.toUpperCase() || 'U'}
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-slate-900 truncate">
                                {user?.email || 'User'}
                            </p>
                            {user?.id && (
                                <p className="text-xs text-slate-500 truncate">
                                    ID: {user.id}
                                </p>
                            )}
                        </div>
                    </div>
                    <Button
                        variant="ghost"
                        size="sm"
                        className="w-full justify-start text-slate-600 hover:text-red-600 hover:bg-red-50"
                        onClick={logout}
                    >
                        <LogOut className="mr-2 h-4 w-4" />
                        Sign Out
                    </Button>
                </div>
            </aside>

            {/* Mobile Header & Content */}
            <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
                {/* Mobile Header */}
                <header className="md:hidden flex items-center justify-between h-16 px-4 border-b border-zinc-200 bg-white">
                    <div className="flex items-center space-x-3">
                        <div className="h-8 w-8 bg-black rounded-lg flex items-center justify-center">
                            <span className="text-white text-lg font-bold">H</span>
                        </div>
                        <span className="text-lg font-bold text-black">H-Cloud</span>
                    </div>
                    <button onClick={() => setMobileMenuOpen(true)}>
                        <Menu className="h-6 w-6 text-zinc-600" />
                    </button>
                </header>

                {/* Mobile Menu Overlay */}
                {mobileMenuOpen && (
                    <div className="fixed inset-0 z-50 md:hidden flex">
                        <div className="fixed inset-0 bg-slate-900/20 backdrop-blur-sm" onClick={() => setMobileMenuOpen(false)} />
                        <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white">
                            <div className="flex items-center justify-between h-16 px-4 border-b border-slate-100">
                                <span className="text-base font-semibold text-slate-900">Navigation</span>
                                <button onClick={() => setMobileMenuOpen(false)}>
                                    <X className="h-5 w-5 text-slate-500" />
                                </button>
                            </div>
                            <nav className="flex-1 p-4 space-y-2">
                                {navItems.map((item) => (
                                    <Link
                                        key={item.path}
                                        to={item.path}
                                        onClick={() => setMobileMenuOpen(false)}
                                        className={cn(
                                            "flex items-center space-x-3 text-sm font-medium rounded-md px-3 py-2",
                                            location.pathname === item.path
                                                ? "bg-slate-100 text-slate-900"
                                                : "text-slate-600 hover:bg-slate-50"
                                        )}
                                    >
                                        <item.icon className="h-4 w-4" />
                                        <span>{item.name}</span>
                                    </Link>
                                ))}
                                <div className="mt-auto pt-4 border-t border-slate-100">
                                    <Button
                                        variant="ghost"
                                        className="w-full justify-start text-slate-600 hover:text-red-600"
                                        onClick={() => {
                                            logout();
                                            setMobileMenuOpen(false);
                                        }}
                                    >
                                        <LogOut className="mr-2 h-4 w-4" />
                                        Sign Out
                                    </Button>
                                </div>
                            </nav>
                        </div>
                    </div>
                )}

                {/* Main Content Area */}
                <main className="flex-1 overflow-auto bg-white p-4 md:p-8">
                    <div className="mx-auto max-w-7xl">
                        <Outlet />
                    </div>
                </main>
            </div>
        </div>
    );
};

export default Layout;
