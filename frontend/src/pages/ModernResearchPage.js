import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Loader2, BookOpen, FileText, CheckCircle, AlertCircle, ExternalLink, Sparkles, Zap, Globe } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { runResearch } from '../utils/api';

const ModernResearchPage = () => {
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [loadingStep, setLoadingStep] = useState(0);

    const loadingSteps = [
        "Initializing autonomous agents...",
        "Crawling trusted sources...",
        "Reading and analyzing content...",
        "Synthesizing insights...",
        "Finalizing report..."
    ];

    useEffect(() => {
        let interval;
        if (loading) {
            setLoadingStep(0);
            interval = setInterval(() => {
                setLoadingStep((prev) => (prev < loadingSteps.length - 1 ? prev + 1 : prev));
            }, 3000);
        }
        return () => clearInterval(interval);
    }, [loading, loadingSteps.length]);

    const handleRunResearch = async () => {
        if (!query.trim()) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const data = await runResearch(query);
            setResult(data);
        } catch (err) {
            setError(err.message || "An unexpected error occurred.");
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') handleRunResearch();
    };

    return (
        <div className="min-h-screen bg-slate-900 text-white overflow-x-hidden selection:bg-blue-500/30">
            {/* Background Gradients */}
            <div className="fixed inset-0 z-0 pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[120px]" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[120px]" />
            </div>

            <div className="relative z-10 container mx-auto px-4 py-12 max-w-5xl">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-center mb-16"
                >
                    <div className="inline-flex items-center justify-center p-2 mb-4 rounded-full bg-blue-500/10 border border-blue-500/20 backdrop-blur-sm">
                        <Sparkles className="w-4 h-4 text-blue-400 mr-2" />
                        <span className="text-sm font-medium text-blue-300">AI-Powered Research Agent</span>
                    </div>
                    <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 tracking-tight">
                        AutoResearcher
                    </h1>
                    <p className="text-xl text-slate-400 max-w-2xl mx-auto">
                        Autonomous multi-source research assistant that crawls, reads, and synthesizes information for you.
                    </p>
                </motion.div>

                {/* Search Section */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="max-w-3xl mx-auto mb-16"
                >
                    <div className="relative group">
                        <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200" />
                        <div className="relative flex items-center bg-slate-800/80 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-2 shadow-2xl">
                            <Search className="w-6 h-6 text-slate-400 ml-4" />
                            <input
                                type="text"
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="What do you want to research? (e.g., 'Future of AI')"
                                className="w-full bg-transparent border-none px-4 py-4 text-lg text-white placeholder-slate-500 focus:outline-none focus:ring-0"
                                disabled={loading}
                            />
                            <button
                                onClick={handleRunResearch}
                                disabled={loading || !query.trim()}
                                className="px-8 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                            >
                                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Zap className="w-5 h-5" />}
                                <span>Research</span>
                            </button>
                        </div>
                    </div>
                </motion.div>

                {/* Loading State */}
                <AnimatePresence>
                    {loading && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="max-w-2xl mx-auto mb-12 text-center"
                        >
                            <div className="flex flex-col items-center gap-4">
                                <div className="relative w-16 h-16">
                                    <div className="absolute inset-0 border-4 border-slate-700 rounded-full" />
                                    <div className="absolute inset-0 border-4 border-blue-500 rounded-full border-t-transparent animate-spin" />
                                    <Globe className="absolute inset-0 m-auto w-6 h-6 text-blue-400 animate-pulse" />
                                </div>
                                <div className="space-y-2">
                                    <h3 className="text-xl font-semibold text-white">{loadingSteps[loadingStep]}</h3>
                                    <p className="text-slate-400 text-sm">Processing vast amounts of data...</p>
                                </div>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Error State */}
                <AnimatePresence>
                    {error && (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            className="max-w-3xl mx-auto mb-12 p-4 bg-red-500/10 border border-red-500/20 rounded-xl flex items-center gap-3 text-red-400"
                        >
                            <AlertCircle className="w-5 h-5 flex-shrink-0" />
                            <p>{error}</p>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Results Section */}
                <AnimatePresence>
                    {result && !loading && (
                        <motion.div
                            initial={{ opacity: 0, y: 40 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5 }}
                            className="space-y-8"
                        >
                            {/* Main Summary Card */}
                            <div className="relative group">
                                <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-purple-500 rounded-2xl blur opacity-10 group-hover:opacity-20 transition duration-500" />
                                <div className="relative bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-8 shadow-xl">
                                    <div className="flex items-center gap-3 mb-6 border-b border-slate-700/50 pb-4">
                                        <div className="p-2 bg-blue-500/20 rounded-lg">
                                            <BookOpen className="w-6 h-6 text-blue-400" />
                                        </div>
                                        <h2 className="text-2xl font-bold text-white">Research Summary</h2>
                                    </div>
                                    <div className="prose prose-invert prose-lg max-w-none">
                                        <ReactMarkdown>{result.summary}</ReactMarkdown>
                                    </div>
                                </div>
                            </div>

                            {/* Grid for Sources & Details */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                {/* Sources Card */}
                                <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 h-full">
                                    <div className="flex items-center gap-3 mb-6">
                                        <div className="p-2 bg-purple-500/20 rounded-lg">
                                            <Globe className="w-5 h-5 text-purple-400" />
                                        </div>
                                        <h3 className="text-xl font-bold text-white">Sources Analyzed</h3>
                                    </div>
                                    <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
                                        {result.sources && result.sources.map((source, idx) => (
                                            <div key={idx} className="group p-4 bg-slate-900/50 rounded-xl border border-slate-700/50 hover:border-blue-500/30 transition-all">
                                                <div className="flex items-start justify-between gap-3">
                                                    <div className="flex-1 min-w-0">
                                                        <h4 className="font-medium text-blue-400 truncate mb-1">Source {idx + 1}</h4>
                                                        <p className="text-xs text-slate-500 truncate">{source.url}</p>
                                                    </div>
                                                    <a href={source.url} target="_blank" rel="noopener noreferrer" className="p-2 hover:bg-slate-800 rounded-lg transition-colors">
                                                        <ExternalLink className="w-4 h-4 text-slate-400 group-hover:text-blue-400" />
                                                    </a>
                                                </div>
                                                <div className="mt-3 text-sm text-slate-400 line-clamp-3 pl-3 border-l-2 border-slate-700">
                                                    {source.cleaned ? source.cleaned.substring(0, 150) + "..." : "No content preview available."}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* Integration Status Card */}
                                <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 h-full">
                                    <div className="flex items-center gap-3 mb-6">
                                        <div className="p-2 bg-green-500/20 rounded-lg">
                                            <CheckCircle className="w-5 h-5 text-green-400" />
                                        </div>
                                        <h3 className="text-xl font-bold text-white">System Status</h3>
                                    </div>
                                    <div className="space-y-4">
                                        <div className="p-4 bg-slate-900/50 rounded-xl border border-slate-700/50">
                                            <pre className="text-xs font-mono text-green-400 whitespace-pre-wrap">
                                                {typeof result.integration_status === 'object'
                                                    ? JSON.stringify(result.integration_status, null, 2)
                                                    : result.integration_status}
                                            </pre>
                                        </div>
                                        <div className="grid grid-cols-2 gap-4">
                                            <div className="p-4 bg-slate-900/50 rounded-xl border border-slate-700/50 text-center">
                                                <div className="text-2xl font-bold text-white mb-1">{result.sources?.length || 0}</div>
                                                <div className="text-xs text-slate-500 uppercase tracking-wider">Sources</div>
                                            </div>
                                            <div className="p-4 bg-slate-900/50 rounded-xl border border-slate-700/50 text-center">
                                                <div className="text-2xl font-bold text-white mb-1">
                                                    {((result.merged_cleaned?.length || 0) / 1000).toFixed(1)}k
                                                </div>
                                                <div className="text-xs text-slate-500 uppercase tracking-wider">Chars Processed</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Raw Data Accordion */}
                            <div className="bg-slate-800/30 backdrop-blur-sm border border-slate-700/30 rounded-2xl overflow-hidden">
                                <details className="group">
                                    <summary className="flex items-center justify-between p-6 cursor-pointer hover:bg-slate-800/50 transition-colors">
                                        <div className="flex items-center gap-3">
                                            <FileText className="w-5 h-5 text-slate-400" />
                                            <span className="font-medium text-slate-300">View Merged Raw Text</span>
                                        </div>
                                        <div className="text-slate-500 group-open:rotate-180 transition-transform">▼</div>
                                    </summary>
                                    <div className="p-6 pt-0 border-t border-slate-700/30 bg-slate-900/50">
                                        <pre className="text-xs text-slate-400 whitespace-pre-wrap font-mono max-h-96 overflow-y-auto mt-4 p-4 bg-black/30 rounded-lg">
                                            {result.merged_cleaned}
                                        </pre>
                                    </div>
                                </details>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
};

export default ModernResearchPage;
