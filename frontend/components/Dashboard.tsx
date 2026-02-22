
import React from 'react';
import { Product, Order } from '../types';
import { LiveDataStream } from './landing/LiveDataStream';
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, ScatterChart, Scatter, ZAxis
} from 'recharts';

interface DashboardProps {
  products: Product[];
  orders: Order[];
  stats: any;
  onSelectProduct: (product: Product) => void;
  onSelectOrder: (order: Order) => void;
  onTabChange: (tab: any) => void;
}

import { apiService } from '../services/api';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

export const Dashboard: React.FC<DashboardProps> = ({ products, orders, stats, onSelectProduct, onSelectOrder, onTabChange }) => {
  const [searchQuery, setSearchQuery] = React.useState('');
  const [analytics, setAnalytics] = React.useState<any>(null);
  const [searchResults, setSearchResults] = React.useState<any>(null);
  const [isSearching, setIsSearching] = React.useState(false);
  const [isLiveStreamActive, setIsLiveStreamActive] = React.useState(false);

  // Draggable button state
  const [streamPosition, setStreamPosition] = React.useState({ x: window.innerWidth - 420, y: 16 });
  const [isDragging, setIsDragging] = React.useState(false);
  const [dragOffset, setDragOffset] = React.useState({ x: 0, y: 0 });
  const streamButtonRef = React.useRef<HTMLDivElement>(null);

  // Drag handlers
  const handleMouseDown = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).tagName === 'BUTTON') return; // Don't drag when clicking the button itself
    
    setIsDragging(true);
    const rect = streamButtonRef.current?.getBoundingClientRect();
    if (rect) {
      setDragOffset({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
      });
    }
  };

  React.useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (isDragging) {
        setStreamPosition({
          x: Math.max(0, Math.min(window.innerWidth - 400, e.clientX - dragOffset.x)),
          y: Math.max(0, Math.min(window.innerHeight - 100, e.clientY - dragOffset.y))
        });
      }
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, dragOffset]);

  React.useEffect(() => {
    // Fetch CSV Analytics
    apiService.getAnalytics().then(setAnalytics).catch(console.error);
  }, []);

  // Enhanced search functionality
  React.useEffect(() => {
    if (searchQuery.trim()) {
      setIsSearching(true);
      
      // Simulate search delay for better UX
      const searchTimeout = setTimeout(() => {
        const results = performSearch(searchQuery, products, orders, stats);
        setSearchResults(results);
        setIsSearching(false);
      }, 300);

      return () => clearTimeout(searchTimeout);
    } else {
      setSearchResults(null);
      setIsSearching(false);
    }
  }, [searchQuery, products, orders, stats]);

  const performSearch = (query: string, products: Product[], orders: Order[], stats: any) => {
    const lowerQuery = query.toLowerCase();
    
    // Search products
    const matchedProducts = products.filter(p =>
      p.name.toLowerCase().includes(lowerQuery) ||
      p.category.toLowerCase().includes(lowerQuery) ||
      p.seller.toLowerCase().includes(lowerQuery) ||
      p.price.toString().includes(lowerQuery) ||
      p.stock.toString().includes(lowerQuery)
    );

    // Search orders
    const matchedOrders = orders.filter(o =>
      o.product.toLowerCase().includes(lowerQuery) ||
      o.status.toLowerCase().includes(lowerQuery) ||
      o.id.toLowerCase().includes(lowerQuery) ||
      o.amount.toString().includes(lowerQuery) ||
      o.date.includes(lowerQuery)
    );

    // Search analytics/stats
    const statsMatches = [];
    if (lowerQuery.includes('revenue') || lowerQuery.includes('ገቢ')) {
      statsMatches.push({ type: 'stat', name: 'Total Revenue', value: `${stats?.totalRevenue || 0} ብር`, action: () => onTabChange('revenue') });
    }
    if (lowerQuery.includes('order') || lowerQuery.includes('ትዕዛዝ')) {
      statsMatches.push({ type: 'stat', name: 'Active Orders', value: stats?.activeOrders || 0, action: () => onTabChange('orders') });
    }
    if (lowerQuery.includes('inventory') || lowerQuery.includes('ክምችት')) {
      statsMatches.push({ type: 'stat', name: 'Inventory Count', value: stats?.inventoryCount || 0, action: () => onTabChange('inventory') });
    }
    if (lowerQuery.includes('alert') || lowerQuery.includes('ማስጠንቀቂያ')) {
      statsMatches.push({ type: 'stat', name: 'Alerts', value: stats?.alertsCount || 0, action: () => onTabChange('alerts') });
    }

    return {
      products: matchedProducts,
      orders: matchedOrders,
      stats: statsMatches,
      totalResults: matchedProducts.length + matchedOrders.length + statsMatches.length
    };
  };

  const totalRevenue = stats?.totalRevenue || orders.reduce((acc, o) => acc + o.amount, 0);
  const lowStockItems = products.filter(p => p.stock < 20);
  const activeOrdersCount = stats?.activeOrders ?? orders.length;

  // Use search results if searching, otherwise show all data
  const filteredProducts = searchResults ? searchResults.products : products;
  const filteredOrders = searchResults ? searchResults.orders : orders;

  // Prepare Chart Data
  const revenueData = React.useMemo(() => {
    const data: any = {};
    orders.forEach(o => {
      if (!data[o.date]) data[o.date] = 0;
      data[o.date] += o.amount;
    });
    return Object.keys(data).map(date => ({ date, revenue: data[date] }));
  }, [orders]);

  const categoryData = React.useMemo(() => {
    const data: any = {};
    products.forEach(p => {
      if (!data[p.category]) data[p.category] = 0;
      data[p.category]++;
    });
    return Object.keys(data).map(name => ({ name, count: data[name] }));
  }, [products]);

  return (
    <div className="p-8 h-full overflow-y-auto custom-scrollbar">
      <div className="max-w-6xl mx-auto">
        {/* Enhanced Search Bar */}
        <div className="mb-8 relative">
          <i className="fas fa-search absolute left-6 top-1/2 -translate-y-1/2 text-slate-400 text-lg"></i>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search products, orders, analytics, or stats... "
            className="w-full bg-white border border-slate-200 rounded-2xl py-5 pl-14 pr-16 text-slate-700 font-medium shadow-sm focus:outline-none focus:ring-4 focus:ring-ethiGreen/5 focus:border-ethiGreen transition-all hover:shadow-md placeholder:text-slate-400 placeholder:font-normal"
          />
          
          {/* Search Status Indicator */}
          <div className="absolute right-6 top-1/2 -translate-y-1/2 flex items-center gap-2">
            {isSearching && (
              <div className="flex items-center gap-2 text-slate-400">
                <i className="fas fa-spinner fa-spin text-sm"></i>
                <span className="text-xs">Searching...</span>
              </div>
            )}
            {searchQuery && !isSearching && searchResults && (
              <div className="flex items-center gap-2 text-ethiGreen">
                <i className="fas fa-check-circle text-sm"></i>
                <span className="text-xs font-medium">{searchResults.totalResults} results</span>
              </div>
            )}
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="w-6 h-6 rounded-full bg-slate-100 hover:bg-slate-200 flex items-center justify-center text-slate-400 hover:text-slate-600 transition-colors"
              >
                <i className="fas fa-times text-xs"></i>
              </button>
            )}
          </div>
        </div>

        {/* Search Results Summary */}
        {searchQuery && searchResults && (
          <div className="mb-8 bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-lg text-slate-800 flex items-center gap-2">
                <i className="fas fa-search text-ethiGreen"></i>
                Search Results for "{searchQuery}"
              </h3>
              <span className="text-sm text-slate-500">
                {searchResults.totalResults} total results
              </span>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Products Results */}
              {searchResults.products.length > 0 && (
                <div className="bg-slate-50 rounded-xl p-4">
                  <h4 className="font-semibold text-slate-700 mb-2 flex items-center gap-2">
                    <i className="fas fa-box text-ethiGreen text-sm"></i>
                    Products ({searchResults.products.length})
                  </h4>
                  <div className="space-y-2">
                    {searchResults.products.slice(0, 3).map((product: Product) => (
                      <div
                        key={product.id}
                        onClick={() => onSelectProduct(product)}
                        className="flex items-center justify-between p-2 bg-white rounded-lg hover:bg-ethiGreen/5 cursor-pointer transition-colors"
                      >
                        <div>
                          <p className="font-medium text-sm text-slate-800">{product.name}</p>
                          <p className="text-xs text-slate-500">{product.category}</p>
                        </div>
                        <span className="text-xs font-bold text-ethiGreen">{product.price} ብር</span>
                      </div>
                    ))}
                    {searchResults.products.length > 3 && (
                      <p className="text-xs text-slate-500 text-center">
                        +{searchResults.products.length - 3} more products
                      </p>
                    )}
                  </div>
                </div>
              )}

              {/* Orders Results */}
              {searchResults.orders.length > 0 && (
                <div className="bg-slate-50 rounded-xl p-4">
                  <h4 className="font-semibold text-slate-700 mb-2 flex items-center gap-2">
                    <i className="fas fa-shopping-cart text-ethiYellow text-sm"></i>
                    Orders ({searchResults.orders.length})
                  </h4>
                  <div className="space-y-2">
                    {searchResults.orders.slice(0, 3).map((order: Order) => (
                      <div
                        key={order.id}
                        onClick={() => onSelectOrder(order)}
                        className="flex items-center justify-between p-2 bg-white rounded-lg hover:bg-ethiYellow/5 cursor-pointer transition-colors"
                      >
                        <div>
                          <p className="font-medium text-sm text-slate-800">{order.product}</p>
                          <p className="text-xs text-slate-500">{order.id}</p>
                        </div>
                        <span className={`text-xs font-bold ${order.status === 'Delivered' ? 'text-green-600' : order.status === 'Pending' ? 'text-orange-600' : 'text-blue-600'}`}>
                          {order.status}
                        </span>
                      </div>
                    ))}
                    {searchResults.orders.length > 3 && (
                      <p className="text-xs text-slate-500 text-center">
                        +{searchResults.orders.length - 3} more orders
                      </p>
                    )}
                  </div>
                </div>
              )}

              {/* Stats Results */}
              {searchResults.stats.length > 0 && (
                <div className="bg-slate-50 rounded-xl p-4">
                  <h4 className="font-semibold text-slate-700 mb-2 flex items-center gap-2">
                    <i className="fas fa-chart-bar text-ethiBlue text-sm"></i>
                    Analytics ({searchResults.stats.length})
                  </h4>
                  <div className="space-y-2">
                    {searchResults.stats.map((stat: any, index: number) => (
                      <div
                        key={index}
                        onClick={stat.action}
                        className="flex items-center justify-between p-2 bg-white rounded-lg hover:bg-ethiBlue/5 cursor-pointer transition-colors"
                      >
                        <p className="font-medium text-sm text-slate-800">{stat.name}</p>
                        <span className="text-xs font-bold text-ethiBlue">{stat.value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {searchResults.totalResults === 0 && (
              <div className="text-center py-8">
                <i className="fas fa-search text-4xl text-slate-300 mb-4"></i>
                <h4 className="font-bold text-slate-600 mb-2">No results found</h4>
                <p className="text-slate-500 text-sm">
                  Try searching for product names, categories, order IDs, or analytics terms like "revenue" or "inventory"
                </p>
              </div>
            )}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Revenue • ገቢ"
            value={`${totalRevenue.toLocaleString()} ብር`}
            icon="fa-money-bill-wave"
            color="text-ethiGreen"
            onClick={() => onTabChange('revenue')}
          />
          <StatCard
            title="Active Orders • ትዕዛዞች"
            value={activeOrdersCount.toString()}
            icon="fa-shopping-cart"
            color="text-ethiYellow"
            onClick={() => onTabChange('orders')}
          />
          <StatCard
            title="Inventory • ክምችት"
            value={(stats?.inventoryCount || products.length).toString()}
            icon="fa-box"
            color="text-ethiGreen"
            onClick={() => onTabChange('inventory')}
          />
          <StatCard
            title="Alerts • ማስጠንቀቂያ"
            value={(stats?.alertsCount || lowStockItems.length).toString()}
            icon="fa-exclamation-triangle"
            color="text-ethiRed"
            onClick={() => onTabChange('alerts')}
          />
        </div>

        {/* CUSTOMER ANALYTICS SECTION */}
        {analytics && analytics.source !== 'mock' && (
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-6">
              <div className="w-1.5 h-6 bg-ethiGreen rounded-full"></div>
              <h3 className="font-bold text-xl text-slate-800">Customer Insights • ደንበኛ ትንተና</h3>
              <span className="text-xs bg-slate-100 text-slate-500 px-2 py-0.5 rounded border border-slate-200">Source: Mall_Customers.csv</span>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* GENDER */}
              <section className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
                <h4 className="font-bold text-sm text-slate-500 uppercase mb-4 text-center">Gender Distribution</h4>
                <div className="h-48">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={analytics.gender_distribution}
                        cx="50%"
                        cy="50%"
                        innerRadius={40}
                        outerRadius={70}
                        paddingAngle={5}
                        dataKey="value"
                      >
                        {analytics.gender_distribution.map((entry: any, index: number) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </section>

              {/* AGE GROUPS */}
              <section className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
                <h4 className="font-bold text-sm text-slate-500 uppercase mb-4 text-center">Age Groups</h4>
                <div className="h-48">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={analytics.age_distribution}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} />
                      <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                      <YAxis hide />
                      <Tooltip cursor={{ fill: 'transparent' }} />
                      <Bar dataKey="count" fill="#8884d8" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </section>

              {/* SPENDING VS INCOME */}
              <section className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
                <h4 className="font-bold text-sm text-slate-500 uppercase mb-4 text-center">Income vs Spending</h4>
                <div className="h-48">
                  <ResponsiveContainer width="100%" height="100%">
                    <ScatterChart>
                      <CartesianGrid />
                      <XAxis type="number" dataKey="x" name="Income" unit="k" tick={{ fontSize: 10 }} />
                      <YAxis type="number" dataKey="y" name="Score" unit="" tick={{ fontSize: 10 }} />
                      <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                      <Scatter name="Customers" data={analytics.spending_vs_income} fill="#009739" />
                    </ScatterChart>
                  </ResponsiveContainer>
                </div>
              </section>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <section className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
            <h3 className="font-bold text-lg mb-6 flex items-center gap-2 px-2">
              <i className="fas fa-chart-line text-ethiGreen"></i> Sales Trends • የሽያጭ ሁኔታ
            </h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={revenueData}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                  <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#64748b' }} />
                  <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#64748b' }} />
                  <Tooltip
                    contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Line type="monotone" dataKey="revenue" stroke="#009739" strokeWidth={3} dot={{ fill: '#009739', strokeWidth: 2 }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </section>

          <section className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
            <h3 className="font-bold text-lg mb-6 flex items-center gap-2 px-2">
              <i className="fas fa-chart-pie text-ethiYellow"></i> Category Distribution • የምርት አይነት
            </h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={categoryData}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#64748b' }} />
                  <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#64748b' }} />
                  <Tooltip
                    cursor={{ fill: '#f1f5f9' }}
                    contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Bar dataKey="count" fill="#FFD100" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </section>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <section className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
            <h3 className="font-bold text-lg mb-6 flex items-center gap-2 px-2">
              <i className="fas fa-list text-ethiGreen"></i> Active Inventory • ንቁ ክምችት
              <span className="ml-auto text-xs font-medium text-slate-400 bg-slate-100 px-2 py-1 rounded-lg">
                {filteredProducts.length} items
              </span>
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="text-slate-400 font-bold uppercase text-[10px] border-b">
                  <tr>
                    <th className="text-left py-3 px-2">Product</th>
                    <th className="text-right py-3 px-2">Stock</th>
                    <th className="text-right py-3 px-2">Price</th>
                    <th className="text-right py-3 px-2">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {filteredProducts.length > 0 ? (
                    filteredProducts.map(p => (
                      <tr key={p.id} className="group hover:bg-slate-50 transition-colors cursor-pointer" onClick={() => onSelectProduct(p)}>
                        <td className="py-4 px-2">
                          <div className="font-semibold text-slate-800">{p.name}</div>
                          <div className="text-[10px] text-slate-400 font-bold uppercase">{p.category}</div>
                        </td>
                        <td className="py-4 px-2 text-right">
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-black uppercase ${p.stock < 20 ? 'bg-orange-100 text-orange-600' : 'bg-emerald-100 text-emerald-600'}`}>
                            {p.stock}
                          </span>
                        </td>
                        <td className="py-4 px-2 text-right font-bold text-slate-700">{p.price.toLocaleString()} ብር</td>
                        <td className="py-4 px-2 text-right">
                          <button className="w-8 h-8 rounded-lg bg-slate-100 text-slate-400 group-hover:bg-indigo-600 group-hover:text-white transition-all">
                            <i className="fas fa-eye text-xs"></i>
                          </button>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={4} className="py-8 text-center text-slate-400">
                        No products found matching "{searchQuery}"
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>

          <section className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
            <h3 className="font-bold text-lg mb-6 flex items-center gap-2 px-2">
              <i className="fas fa-history text-ethiGreen"></i> Recent Orders • የቅርብ ጊዜ ትዕዛዞች
              <span className="ml-auto text-xs font-medium text-slate-400 bg-slate-100 px-2 py-1 rounded-lg">
                {filteredOrders.length} orders
              </span>
            </h3>
            <div className="space-y-4">
              {filteredOrders.length > 0 ? (
                filteredOrders.map(o => (
                  <div
                    key={o.id}
                    onClick={() => onSelectOrder(o)}
                    className="flex items-center justify-between p-4 bg-slate-50 rounded-2xl border border-slate-100 hover:border-indigo-200 hover:bg-indigo-50/30 transition-all cursor-pointer group"
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center border border-slate-200 shadow-sm group-hover:border-indigo-100">
                        <i className="fas fa-box-open text-slate-400 group-hover:text-indigo-500"></i>
                      </div>
                      <div>
                        <p className="font-bold text-sm text-slate-800">{o.product}</p>
                        <p className="text-[10px] text-slate-400 font-bold uppercase">{o.id} • {o.date}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-ethiGreen">{o.amount.toLocaleString()} ብር</p>
                      <span className={`text-[10px] font-black uppercase tracking-widest ${o.status === 'Delivered' ? 'text-emerald-500' : o.status === 'Pending' ? 'text-orange-500' : 'text-blue-500'}`}>
                        {o.status}
                      </span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="py-8 text-center text-slate-400">
                  No orders found matching "{searchQuery}"
                </div>
              )}
            </div>
          </section>
        </div>
      </div>

      {/* Live Data Stream Overlay - Draggable */}
      <div 
        ref={streamButtonRef}
        style={{
          position: 'fixed',
          top: streamPosition.y + 'px',
          left: streamPosition.x + 'px',
          zIndex: 50,
          cursor: isDragging ? 'grabbing' : 'grab',
        }}
        onMouseDown={handleMouseDown}
      >
        {/* Start/Stop Button */}
        <button
          onClick={() => setIsLiveStreamActive(!isLiveStreamActive)}
          className={`mb-4 px-4 py-2 rounded-xl font-semibold transition-all duration-300 shadow-lg ${
            isLiveStreamActive 
              ? 'bg-red-500 hover:bg-red-600 text-white' 
              : 'bg-ethiGreen hover:bg-emerald-600 text-white'
          }`}
        >
          <i className={`fas ${isLiveStreamActive ? 'fa-stop' : 'fa-play'} mr-2`}></i>
          {isLiveStreamActive ? 'Stop Stream' : 'Start Live Stream'}
        </button>

        {/* Transparent Live Data Stream Overlay */}
        {isLiveStreamActive && (
          <div className="w-96 h-[500px] bg-white/90 backdrop-blur-md rounded-2xl shadow-2xl border border-white/20">
            <LiveDataStream isActive={isLiveStreamActive} />
          </div>
        )}
      </div>
    </div>
  );
};


const StatCard = ({ title, value, icon, color, onClick }: any) => (
  <div
    onClick={onClick}
    className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm transition-all hover:shadow-lg hover:-translate-y-1 cursor-pointer group"
  >
    <div className={`w-10 h-10 ${color} bg-opacity-10 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
      <i className={`fas ${icon}`}></i>
    </div>
    <p className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">{title}</p>
    <p className="text-2xl font-black text-slate-800 tracking-tighter">{value}</p>
  </div>
);
