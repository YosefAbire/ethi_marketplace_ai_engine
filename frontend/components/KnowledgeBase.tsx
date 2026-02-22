import React from 'react';
import { Document } from '../types';

interface KBProps {
  documents: Document[];
  onFileUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onDeleteDocument: (id: string) => void;
}

export const KnowledgeBase: React.FC<KBProps> = ({ documents, onFileUpload, onDeleteDocument }) => {
  return (
    <div className="p-8 h-full overflow-y-auto custom-scrollbar">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-10">
          <div>
            <h2 className="text-3xl font-black text-slate-800 tracking-tight">Knowledge Base • የእውቀት ማከማቻ</h2>
            <p className="text-slate-500 font-medium whitespace-nowrap overflow-hidden text-ellipsis">Manage context for the RAG Agent. Documents are saved locally.</p>
          </div>
          <label className="cursor-pointer bg-ethiGreen text-white px-6 py-3 rounded-2xl hover:bg-ethiGreen/80 shadow-lg shadow-ethiGreen/10 transition-all font-bold flex items-center gap-2">
            <i className="fas fa-cloud-upload-alt"></i> Upload • ሰነድ ጫን
            <input
              type="file"
              multiple
              className="hidden"
              onChange={onFileUpload}
              onClick={(e) => (e.target as HTMLInputElement).value = ''}
              accept=".pdf,.csv,.txt,.docx"
            />
          </label>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {documents.length === 0 ? (
            <div className="col-span-full py-32 bg-white rounded-[40px] border-2 border-dashed border-slate-200 flex flex-col items-center justify-center text-slate-400">
              <i className="fas fa-folder-open text-6xl mb-6 opacity-20"></i>
              <p className="font-bold text-lg">Knowledge base is empty</p>
              <p className="text-sm">Upload PDFs, CSVs or TXT files to provide context for your agents.</p>
            </div>
          ) : (
            documents.map(doc => (
              <div key={doc.id} className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm hover:shadow-md transition-all group overflow-hidden relative">
                <div className="absolute top-0 right-0 p-4 opacity-5 scale-150 rotate-12 group-hover:scale-[2] transition-transform">
                  <i className="fas fa-file-alt text-6xl"></i>
                </div>
                <div className="flex items-center justify-between mb-4 relative z-10">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-slate-50 border border-slate-100 rounded-2xl flex items-center justify-center text-ethiGreen">
                      <i className={`fas ${doc.name.toLowerCase().endsWith('.pdf') ? 'fa-file-pdf' : 'fa-file-alt'} text-xl`}></i>
                    </div>
                    <div className="min-w-0">
                      <h4 className="font-bold text-slate-800 truncate text-sm w-40">{doc.name}</h4>
                      <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{doc.size} • {doc.type.split('/')[1]?.toUpperCase() || 'TXT'}</p>
                    </div>
                  </div>
                  <button
                    onClick={(e) => { e.stopPropagation(); onDeleteDocument(doc.id); }}
                    className="w-8 h-8 rounded-full flex items-center justify-center text-slate-300 hover:text-red-500 hover:bg-red-50 transition-all pointer-events-auto"
                    title="Delete document"
                  >
                    <i className="fas fa-trash-alt text-xs"></i>
                  </button>
                </div>
                <div className="h-24 bg-slate-50 rounded-2xl p-4 text-[10px] font-mono text-slate-400 overflow-hidden relative">
                  {doc.content}
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-50 via-transparent to-transparent"></div>
                </div>
                <div className="mt-4 pt-4 border-t border-slate-100 flex justify-between items-center">
                  <span className="text-[10px] text-slate-400 font-bold uppercase">Added {doc.uploadedAt.toLocaleDateString()}</span>
                  <button className="text-xs font-bold text-ethiGreen hover:underline">View Extract • ሙሉ እይታ</button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};