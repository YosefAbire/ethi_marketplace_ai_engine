import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

interface AuthPageProps {
    onLogin: (user: any) => void;
    onBack: () => void;
}

export const AuthPage: React.FC<AuthPageProps> = ({ onLogin, onBack }) => {
    const { login, signup } = useAuth();
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({ email: '', password: '', name: '' });
    const [loading, setLoading] = useState(false);

    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            let userData;
            if (isLogin) {
                const userCredential: any = await login(formData.email, formData.password);
                userData = {
                    name: userCredential.user.displayName || userCredential.user.email,
                    email: userCredential.user.email,
                    uid: userCredential.user.uid
                };
            } else {
                const userCredential: any = await signup(formData.name, formData.email, formData.password);
                userData = {
                    name: formData.name,
                    email: userCredential.user.email,
                    uid: userCredential.user.uid
                };
            }

            localStorage.setItem('ethi_market_user', JSON.stringify(userData));
            onLogin(userData);
        } catch (err: any) {
            setError(err.message || 'Authentication failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center p-8 relative overflow-y-auto font-inter custom-scrollbar">
            <div className="absolute inset-0 tibeb-bg opacity-5 pointer-events-none"></div>

            <div className="flex flex-col items-center gap-8 relative z-10 w-full max-w-md">
                {/* Back Button */}
                <button
                    onClick={onBack}
                    className="self-start px-6 py-3 bg-white rounded-2xl shadow-sm border border-slate-200 text-slate-500 hover:text-ethiGreen transition-all flex items-center gap-3 font-bold text-xs group hover:shadow-md"
                >
                    <i className="fas fa-arrow-left transition-transform group-hover:-translate-x-1"></i>
                    <span>Back to Landing • ተመለስ</span>
                </button>

                <div className="w-full bg-white rounded-[3rem] shadow-3xl border border-slate-100 p-12 transition-all">
                    <div className="flex flex-col items-center mb-10 text-center">
                        <div className="w-16 h-16 bg-ethiGreen rounded-2xl flex items-center justify-center text-white shadow-xl shadow-ethiGreen/20 mb-6">
                            <i className="fas fa-key text-2xl"></i>
                        </div>
                        <h2 className="text-3xl font-black tracking-tight text-slate-800">
                            {isLogin ? 'Welcome Back • ሰላም' : 'Create Account • ክፈት'}
                        </h2>
                        <p className="text-slate-400 text-sm font-medium mt-2">
                            {isLogin ? 'Login to manage your marketplace' : 'Join the Ethiopian AI marketplace engine'}
                        </p>
                        {error && (
                            <div className="mt-4 p-3 bg-red-50 border border-red-100 text-red-600 text-xs font-bold rounded-xl animate-shake">
                                <i className="fas fa-circle-exclamation mr-2"></i>
                                {error}
                            </div>
                        )}
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        {!isLogin && (
                            <div className="space-y-2">
                                <label htmlFor="name-input" className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Full Name</label>
                                <div className="relative">
                                    <i className="fas fa-user absolute left-5 top-1/2 -translate-y-1/2 text-slate-300"></i>
                                    <input
                                        id="name-input"
                                        type="text"
                                        required
                                        value={formData.name}
                                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                        placeholder="Enter your name"
                                        className="w-full pl-12 pr-6 py-4 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-4 focus:ring-ethiGreen/5 focus:border-ethiGreen transition-all font-medium text-sm"
                                    />
                                </div>
                            </div>
                        )}

                        <div className="space-y-2">
                            <label htmlFor="email-input" className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Email Address</label>
                            <div className="relative">
                                <i className="fas fa-envelope absolute left-5 top-1/2 -translate-y-1/2 text-slate-300"></i>
                                <input
                                    id="email-input"
                                    type="email"
                                    required
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    placeholder="email@example.com"
                                    className="w-full pl-12 pr-6 py-4 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-4 focus:ring-ethiGreen/5 focus:border-ethiGreen transition-all font-medium text-sm"
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label htmlFor="password-input" className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Secret Key / Password</label>
                            <div className="relative">
                                <i className="fas fa-lock absolute left-5 top-1/2 -translate-y-1/2 text-slate-300"></i>
                                <input
                                    id="password-input"
                                    type="password"
                                    required
                                    value={formData.password}
                                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                    placeholder="••••••••"
                                    className="w-full pl-12 pr-6 py-4 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-4 focus:ring-ethiGreen/5 focus:border-ethiGreen transition-all font-medium text-sm"
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-5 bg-ethiGreen text-white rounded-2xl font-black text-sm hover:bg-ethiGreen/90 shadow-2xl shadow-ethiGreen/20 transition-all flex items-center justify-center gap-3 disabled:opacity-50"
                        >
                            {loading ? (
                                <i className="fas fa-circle-notch fa-spin text-lg"></i>
                            ) : (
                                <>
                                    <span>{isLogin ? 'Login Now • ግባ' : 'Create Account • ጨርስ'}</span>
                                    <i className="fas fa-arrow-right"></i>
                                </>
                            )}
                        </button>
                    </form>

                    <div className="mt-8 pt-8 border-t border-slate-100 text-center">
                        <button
                            onClick={() => setIsLogin(!isLogin)}
                            className="text-sm font-bold text-slate-500 hover:text-ethiGreen transition-colors"
                        >
                            {isLogin ? "Don't have an account? Register" : "Already have an account? Login"}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};
