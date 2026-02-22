
import React from 'react';
import { Product, Order } from '../types';

interface ProductModalProps {
  product: Product;
  onClose: () => void;
}

export const ProductModal: React.FC<ProductModalProps> = ({ product, onClose }) => {
  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white w-full max-w-2xl rounded-[2.5rem] shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
        <div className="relative h-48 bg-gradient-to-br from-ethiGreen to-ethiDark p-8 flex items-end">
          <button
            onClick={onClose}
            className="absolute top-6 right-6 w-10 h-10 bg-white/20 hover:bg-white/30 text-white rounded-full flex items-center justify-center backdrop-blur-md transition-all"
          >
            <i className="fas fa-times"></i>
          </button>
          <div className="flex items-center gap-6">
            <div className="w-24 h-24 bg-white rounded-3xl shadow-xl flex items-center justify-center text-ethiGreen">
              <i className="fas fa-box-open text-4xl"></i>
            </div>
            <div className="text-white">
              <span className="text-[10px] font-black uppercase tracking-widest opacity-80">{product.category}</span>
              <h2 className="text-3xl font-black tracking-tight">{product.name}</h2>
            </div>
          </div>
        </div>

        <div className="p-10 grid grid-cols-2 gap-8">
          <div className="space-y-6">
            <div>
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Price & Rating</p>
              <div className="flex items-center gap-4">
                <span className="text-2xl font-black text-slate-800">{product.price.toLocaleString()} ብር</span>
                <div className="flex items-center gap-1 text-amber-500 font-bold">
                  {product.rating} <i className="fas fa-star text-xs"></i>
                </div>
              </div>
            </div>
            <div>
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Inventory Status</p>
              <div className="flex items-center gap-2">
                <span className={`px-3 py-1 rounded-lg text-xs font-black ${product.stock < 20 ? 'bg-orange-100 text-orange-600' : 'bg-emerald-100 text-emerald-600'}`}>
                  {product.stock} UNITS IN STOCK
                </span>
                {product.stock < 20 && <i className="fas fa-exclamation-triangle text-orange-500 animate-pulse"></i>}
              </div>
            </div>
            <div>
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Seller Identity</p>
              <div className="flex items-center gap-2 text-slate-700 font-bold">
                <i className="fas fa-store text-indigo-500"></i>
                {product.seller}
              </div>
            </div>
          </div>

          <div className="space-y-6 border-l pl-8 border-slate-100">
            <div>
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Specifications</p>
              <ul className="space-y-3">
                <li className="flex justify-between text-sm">
                  <span className="text-slate-400">SKU</span>
                  <span className="font-mono font-bold text-slate-700">{product.sku || `ETHI-${product.id}`}</span>
                </li>
                <li className="flex justify-between text-sm">
                  <span className="text-slate-400">Origin</span>
                  <span className="font-bold text-slate-700">{product.origin || 'Ethiopia'}</span>
                </li>
              </ul>
            </div>
            <div>
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Description</p>
              <p className="text-sm text-slate-500 leading-relaxed italic">
                {product.description || `Premium quality ${product.name.toLowerCase()} sourced directly from the heart of the marketplace. Certified organic and ethically produced.`}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-slate-50 p-6 flex justify-end gap-4">
          <button className="px-6 py-3 rounded-2xl bg-slate-200 text-slate-600 font-bold text-sm hover:bg-slate-300 transition-all">Export PDF</button>
          <button className="px-8 py-3 rounded-2xl bg-ethiGreen text-white font-black text-sm hover:bg-ethiGreen/80 shadow-lg shadow-ethiGreen/10 transition-all">Edit Product</button>
        </div>
      </div>
    </div>
  );
};

interface OrderModalProps {
  order: Order;
  onClose: () => void;
}

export const OrderModal: React.FC<OrderModalProps> = ({ order, onClose }) => {
  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white w-full max-w-xl rounded-[2.5rem] shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
        <div className="p-8 border-b flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-black tracking-tight text-slate-800">Order Details</h2>
            <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">{order.id} • {order.date}</p>
          </div>
          <button
            onClick={onClose}
            className="w-10 h-10 bg-slate-100 hover:bg-slate-200 text-slate-500 rounded-full flex items-center justify-center transition-all"
          >
            <i className="fas fa-times"></i>
          </button>
        </div>

        <div className="p-10 space-y-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-slate-50 border border-slate-100 rounded-2xl flex items-center justify-center text-ethiGreen">
                <i className="fas fa-shopping-bag text-2xl"></i>
              </div>
              <div>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-0.5">Purchased Item</p>
                <h3 className="font-black text-lg text-slate-800">{order.product}</h3>
              </div>
            </div>
            <div className="text-right">
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-0.5">Total Amount</p>
              <p className="text-2xl font-black text-ethiGreen">{order.amount.toLocaleString()} ብር</p>
            </div>
          </div>

          <div className="bg-slate-50 rounded-3xl p-6 border border-slate-100">
            <div className="grid grid-cols-2 gap-6">
              <div>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Fulfillment Status</p>
                <span className={`inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-black uppercase tracking-widest ${order.status === 'Delivered' ? 'bg-emerald-100 text-emerald-600' :
                    order.status === 'Shipped' ? 'bg-blue-100 text-blue-600' :
                      'bg-orange-100 text-orange-600'
                  }`}>
                  <span className={`w-2 h-2 rounded-full ${order.status === 'Delivered' ? 'bg-emerald-500' :
                      order.status === 'Shipped' ? 'bg-blue-500' :
                        'bg-orange-500'
                    }`}></span>
                  {order.status}
                </span>
              </div>
              <div>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Tracking Number</p>
                <p className="font-mono font-bold text-slate-700">{order.trackingId || `ETH-TRK-${Math.floor(Math.random() * 1000000)}`}</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <i className="fas fa-user text-slate-300 mt-1"></i>
              <div>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Customer</p>
                <p className="text-sm font-bold text-slate-700">{order.customerName || 'Abebe Bikila'}</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <i className="fas fa-location-dot text-slate-300 mt-1"></i>
              <div>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Shipping Address</p>
                <p className="text-sm font-bold text-slate-700">{order.shippingAddress || 'Bole, Addis Ababa, Ethiopia'}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="p-8 border-t bg-white flex items-center justify-between">
          <button className="text-xs font-black text-indigo-600 hover:text-indigo-800 uppercase tracking-widest flex items-center gap-2">
            <i className="fas fa-envelope"></i> Send Receipt
          </button>
          <button className="px-8 py-4 bg-slate-900 text-white rounded-2xl font-black text-sm hover:bg-black transition-all shadow-xl shadow-slate-100">
            Track Package
          </button>
        </div>
      </div>
    </div>
  );
};
