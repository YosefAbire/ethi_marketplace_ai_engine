
import React from 'react';
import { Product, Order } from '../types';

interface MetricPageProps {
    onBack: () => void;
}

export const RevenuePage: React.FC<MetricPageProps & { orders: Order[] }> = ({ onBack, orders }) => {
    const total = orders.reduce((acc, o) => acc + o.amount, 0);
    return (
        <div className="p-8 h-full overflow-y-auto bg-white rounded-3xl m-4 border border-slate-200">
            <header className="flex items-center gap-4 mb-10">
                <button onClick={onBack} className="w-10 h-10 bg-slate-100 rounded-xl flex items-center justify-center text-slate-500 hover:bg-ethiGreen hover:text-white transition-all shadow-sm">
                    <i className="fas fa-arrow-left"></i>
                </button>
                <div>
                    <h2 className="text-2xl font-black text-slate-800 tracking-tight">Financial Overview • የፋይናንስ አጠቃላይ እይታ</h2>
                    <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Revenue Analytics & Transaction History</p>
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                <div className="p-6 bg-emerald-50 border border-emerald-100 rounded-3xl">
                    <p className="text-[10px] font-black text-emerald-600 uppercase tracking-[0.2em] mb-2">Total Revenue</p>
                    <p className="text-3xl font-black text-emerald-700">{total.toLocaleString()} ብር</p>
                </div>
                <div className="p-6 bg-slate-50 border border-slate-100 rounded-3xl">
                    <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-2">Total Transactions</p>
                    <p className="text-3xl font-black text-slate-700">{orders.length}</p>
                </div>
                <div className="p-6 bg-slate-50 border border-slate-100 rounded-3xl">
                    <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-2">Average Order Value</p>
                    <p className="text-3xl font-black text-slate-700">{orders.length > 0 ? (total / orders.length).toFixed(2) : 0} ብር</p>
                </div>
            </div>

            <div className="bg-white rounded-3xl border border-slate-100 overflow-hidden shadow-sm">
                <table className="w-full text-sm">
                    <thead className="bg-slate-50 border-b border-slate-100 text-slate-400 font-bold uppercase text-[10px]">
                        <tr>
                            <th className="text-left py-4 px-6 tracking-widest">Transaction ID</th>
                            <th className="text-left py-4 px-6 tracking-widest">Product</th>
                            <th className="text-left py-4 px-6 tracking-widest">Date</th>
                            <th className="text-right py-4 px-6 tracking-widest">Amount</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-50">
                        {orders.map(o => (
                            <tr key={o.id} className="hover:bg-slate-50 transition-colors">
                                <td className="py-4 px-6 font-mono text-xs text-slate-500">{o.id}</td>
                                <td className="py-4 px-6 font-bold text-slate-700">{o.product}</td>
                                <td className="py-4 px-6 text-slate-500">{o.date}</td>
                                <td className="py-4 px-6 text-right font-black text-ethiGreen">{o.amount.toLocaleString()} ብር</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export const ActiveOrdersPage: React.FC<MetricPageProps & { orders: Order[] }> = ({ onBack, orders }) => {
    const active = orders.filter(o => o.status !== 'Delivered');
    return (
        <div className="p-8 h-full overflow-y-auto bg-white rounded-3xl m-4 border border-slate-200">
            <header className="flex items-center gap-4 mb-10">
                <button onClick={onBack} className="w-10 h-10 bg-slate-100 rounded-xl flex items-center justify-center text-slate-500 hover:bg-ethiYellow hover:text-white transition-all shadow-sm">
                    <i className="fas fa-arrow-left"></i>
                </button>
                <div>
                    <h2 className="text-2xl font-black text-slate-800 tracking-tight">Active Orders • ንቁ ትዕዛዞች</h2>
                    <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Live Logistics & fulfillment tracking</p>
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-10">
                {['Pending', 'Shipped', 'Delivered'].map(status => (
                    <div key={status} className="p-6 bg-slate-50 rounded-3xl border border-slate-100">
                        <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">{status}</p>
                        <p className="text-3xl font-black text-slate-700">{orders.filter(o => o.status === status).length}</p>
                    </div>
                ))}
            </div>

            <div className="space-y-4">
                {active.map(o => (
                    <div key={o.id} className="flex items-center justify-between p-6 bg-slate-50 rounded-[2rem] border border-slate-100">
                        <div className="flex items-center gap-6">
                            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-white shadow-lg ${o.status === 'Shipped' ? 'bg-blue-500 shadow-blue-200' : 'bg-orange-500 shadow-orange-200'}`}>
                                <i className={`fas ${o.status === 'Shipped' ? 'fa-truck' : 'fa-clock'}`}></i>
                            </div>
                            <div>
                                <p className="font-black text-lg text-slate-800">{o.product}</p>
                                <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">{o.id} • Expected delivery: Tomorrow</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-8">
                            <div className="text-right">
                                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Current Status</p>
                                <span className={`text-sm font-black uppercase ${o.status === 'Shipped' ? 'text-blue-500' : 'text-orange-500'}`}>{o.status}</span>
                            </div>
                            <div className="w-px h-10 bg-slate-200"></div>
                            <div className="text-right">
                                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Value</p>
                                <p className="font-black text-ethiGreen">{o.amount.toLocaleString()} ብር</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export const InventoryPage: React.FC<MetricPageProps & { products: Product[] }> = ({ onBack, products }) => {
    return (
        <div className="p-8 h-full overflow-y-auto bg-white rounded-3xl m-4 border border-slate-200">
            <header className="flex items-center gap-4 mb-10">
                <button onClick={onBack} className="w-10 h-10 bg-slate-100 rounded-xl flex items-center justify-center text-slate-500 hover:bg-ethiGreen hover:text-white transition-all shadow-sm">
                    <i className="fas fa-arrow-left"></i>
                </button>
                <div>
                    <h2 className="text-2xl font-black text-slate-800 tracking-tight">Inventory Management • የክምችት አስተዳደር</h2>
                    <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Full Stock Catalog & SKU Management</p>
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {products.map(p => (
                    <div key={p.id} className="p-6 bg-slate-50 rounded-3xl border border-slate-100 group hover:border-ethiGreen hover:shadow-xl hover:shadow-ethiGreen/5 transition-all">
                        <div className="flex justify-between items-start mb-4">
                            <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center shadow-sm group-hover:scale-110 transition-transform">
                                <i className="fas fa-box text-ethiGreen text-xl"></i>
                            </div>
                            <div className="text-right">
                                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Stock Level</p>
                                <p className={`text-xl font-black ${p.stock < 20 ? 'text-orange-500' : 'text-emerald-500'}`}>{p.stock}</p>
                            </div>
                        </div>
                        <h4 className="font-black text-slate-800 text-lg mb-1">{p.name}</h4>
                        <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-4">{p.category} • {p.seller}</p>
                        <div className="pt-4 border-t border-slate-200 flex justify-between items-center">
                            <p className="font-black text-ethiGreen">{p.price.toLocaleString()} ብር</p>
                            <div className="flex items-center gap-1 text-ethiYellow">
                                <i className="fas fa-star text-[10px]"></i>
                                <span className="text-xs font-black text-slate-600">{p.rating}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export const AlertsPage: React.FC<MetricPageProps & { products: Product[] }> = ({ onBack, products }) => {
    const alerts = products.filter(p => p.stock < 20);
    return (
        <div className="p-8 h-full overflow-y-auto bg-white rounded-3xl m-4 border border-slate-200">
            <header className="flex items-center gap-4 mb-10">
                <button onClick={onBack} className="w-10 h-10 bg-slate-100 rounded-xl flex items-center justify-center text-slate-500 hover:bg-ethiRed hover:text-white transition-all shadow-sm">
                    <i className="fas fa-arrow-left"></i>
                </button>
                <div>
                    <h2 className="text-2xl font-black text-slate-800 tracking-tight">Operational Alerts • ማስጠንቀቂያዎች</h2>
                    <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Critical action items and warnings</p>
                </div>
            </header>

            <div className="space-y-4">
                {alerts.map(p => (
                    <div key={p.id} className="p-6 bg-red-50 border border-red-100 rounded-3xl flex items-center justify-between animate-pulse-subtle">
                        <div className="flex items-center gap-6">
                            <div className="w-14 h-14 bg-red-500 text-white rounded-2xl flex items-center justify-center shadow-lg shadow-red-200">
                                <i className="fas fa-triangle-exclamation text-xl"></i>
                            </div>
                            <div>
                                <p className="font-black text-lg text-red-900">Low Stock: {p.name}</p>
                                <p className="text-xs font-bold text-red-600 uppercase tracking-widest">Only {p.stock} units remaining in inventory</p>
                            </div>
                        </div>
                        <button className="px-6 py-3 bg-red-600 text-white rounded-xl font-bold text-sm hover:bg-red-700 transition-all shadow-lg shadow-red-200 uppercase tracking-widest">
                            Restock Now
                        </button>
                    </div>
                ))}
                {alerts.length === 0 && (
                    <div className="py-20 text-center">
                        <div className="w-20 h-20 bg-emerald-50 text-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6">
                            <i className="fas fa-check-circle text-4xl"></i>
                        </div>
                        <h3 className="text-xl font-black text-slate-800 mb-2">Systems Normal • ሁሉም ነገር ሰላም ነው</h3>
                        <p className="text-slate-400 font-medium">No critical alerts or low stock items detected.</p>
                    </div>
                )}
            </div>
        </div>
    );
};
