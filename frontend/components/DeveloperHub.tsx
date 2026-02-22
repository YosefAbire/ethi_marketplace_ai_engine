
import React, { useState, useEffect } from 'react';
import { gemini } from '../services/gemini';

export const DeveloperHub: React.FC = () => {
  const [code, setCode] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    gemini.generateBackendCode()
      .then(res => setCode(res))
      .catch(err => setCode("# Error loading code."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="p-8 h-full overflow-y-auto">
      <div className="max-w-5xl mx-auto">
        <h2 className="text-3xl font-black mb-8">Developer Hub • የልማት ማዕከል</h2>
        <div className="bg-slate-900 rounded-[40px] p-8 border border-slate-800">
          {loading ? <p className="text-ethiGreen/50 animate-pulse">Loading code • በማውረድ ላይ...</p> : (
            <pre className="text-ethiGreen font-mono text-xs whitespace-pre-wrap">{code}</pre>
          )}
        </div>
      </div>
    </div>
  );
};
