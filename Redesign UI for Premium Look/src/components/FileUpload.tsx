import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Upload, Link as LinkIcon, Sparkles, AlertTriangle, FileText, Check } from "lucide-react";
import { Button } from "./ui/button";
import { Alert, AlertDescription } from "./ui/alert";

export function FileUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const [url, setUrl] = useState("");

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const containerVariants = {
    hidden: { opacity: 0, y: 40 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.8,
        ease: [0.16, 1, 0.3, 1],
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: [0.16, 1, 0.3, 1],
      },
    },
  };

  return (
    <motion.div
      className="space-y-10"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* URL Input Section */}
      <motion.div variants={itemVariants}>
        <div className="flex items-center gap-4">
          <div className="flex-1 relative group">
            <div className="absolute -inset-[1px] bg-gradient-to-r from-indigo-500/0 to-purple-500/0 group-focus-within:from-indigo-500/50 group-focus-within:to-purple-500/50 rounded-2xl blur-xl transition-all duration-500"></div>
            <div className="relative flex items-center gap-4 bg-white/[0.02] border border-white/5 group-focus-within:border-white/20 rounded-2xl p-2 backdrop-blur-xl transition-all duration-300">
              <div className="flex items-center justify-center size-12 bg-gradient-to-br from-indigo-500/10 to-purple-500/10 rounded-xl ml-1 border border-white/5">
                <LinkIcon className="size-5 text-indigo-400" strokeWidth={2} />
              </div>
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Paste a URL to analyze (e.g., https://example.com/document)"
                className="flex-1 bg-transparent outline-none py-3 pr-4 text-sm text-white/90 placeholder:text-white/30"
              />
            </div>
          </div>

          <Button className="h-[72px] px-8 gap-2 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 hover:from-indigo-600 hover:via-purple-600 hover:to-pink-600 text-white rounded-2xl shadow-2xl shadow-indigo-500/25 transition-all duration-300 hover:shadow-indigo-500/40 hover:scale-[1.02] group relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
            <Sparkles className="size-5" strokeWidth={2} />
            <span className="text-sm">Analyze</span>
          </Button>
        </div>

        {/* Security Warning */}
        <Alert className="mt-6 border-amber-500/20 bg-amber-500/5 backdrop-blur-xl">
          <AlertTriangle className="size-4 text-amber-400" strokeWidth={2} />
          <AlertDescription className="text-xs text-amber-200/70">
            <strong className="text-amber-200">Note:</strong> Sites with heavy security (banking, e-commerce, protected portals) may not work.
          </AlertDescription>
        </Alert>
      </motion.div>

      {/* Divider */}
      <motion.div variants={itemVariants} className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-white/5"></div>
        </div>
        <div className="relative flex justify-center text-xs">
          <span className="px-6 bg-[#0A0A0F] text-white/30 uppercase tracking-widest">Or upload a file</span>
        </div>
      </motion.div>

      {/* File Upload Drop Zone */}
      <motion.div
        variants={itemVariants}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className="relative group"
      >
        <AnimatePresence>
          {isDragging && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-gradient-to-br from-indigo-500/20 via-purple-500/20 to-pink-500/20 rounded-3xl z-10 flex items-center justify-center border-2 border-indigo-400/50 border-dashed backdrop-blur-xl"
            >
              <div className="text-center">
                <Upload className="size-16 text-indigo-400 mx-auto mb-4" strokeWidth={1.5} />
                <p className="text-white/90">Drop your file here</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="relative border-2 border-dashed border-white/10 rounded-3xl p-20 bg-white/[0.01] hover:border-white/20 hover:bg-white/[0.02] transition-all duration-500 cursor-pointer group">
          <div className="absolute -inset-[1px] bg-gradient-to-br from-indigo-500/0 via-purple-500/0 to-pink-500/0 group-hover:from-indigo-500/20 group-hover:via-purple-500/20 group-hover:to-pink-500/20 rounded-3xl blur-2xl transition-all duration-700"></div>

          <div className="relative flex flex-col items-center justify-center text-center space-y-8">
            <motion.div
              animate={{
                y: [0, -12, 0],
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                ease: "easeInOut",
              }}
              className="relative"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-2xl blur-2xl opacity-40"></div>
              <div className="relative bg-gradient-to-br from-white/5 to-white/[0.02] p-8 rounded-2xl border border-white/10 backdrop-blur-xl">
                <FileText className="size-16 text-white/90" strokeWidth={1.5} />
              </div>
            </motion.div>

            <div className="space-y-4">
              <p className="text-lg text-white/90">
                <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                  Click to select
                </span>
                <span className="text-white/40"> or drag and drop</span>
              </p>
              <div className="flex items-center justify-center gap-3 text-xs text-white/50">
                <div className="flex items-center gap-1.5 px-4 py-2 bg-white/[0.03] rounded-full border border-white/5">
                  <Check className="size-3 text-indigo-400" strokeWidth={3} />
                  <span>PDF</span>
                </div>
                <div className="flex items-center gap-1.5 px-4 py-2 bg-white/[0.03] rounded-full border border-white/5">
                  <Check className="size-3 text-purple-400" strokeWidth={3} />
                  <span>Excel</span>
                </div>
                <div className="flex items-center gap-1.5 px-4 py-2 bg-white/[0.03] rounded-full border border-white/5">
                  <Check className="size-3 text-pink-400" strokeWidth={3} />
                  <span>DOCX</span>
                </div>
                <div className="flex items-center gap-1.5 px-4 py-2 bg-white/[0.03] rounded-full border border-white/5">
                  <Check className="size-3 text-rose-400" strokeWidth={3} />
                  <span>CSV</span>
                </div>
              </div>
              <p className="text-xs text-white/30 pt-2">
                Supported formats: PDF, Excel (XLSX, XLS), CSV, DOCX, TXT
              </p>
            </div>
          </div>

          <input
            type="file"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            accept=".pdf,.xlsx,.xls,.csv,.docx,.txt"
          />
        </div>
      </motion.div>

      {/* Feature Cards */}
      <motion.div variants={itemVariants} className="grid grid-cols-3 gap-6 pt-4">
        <motion.div
          whileHover={{ y: -4, scale: 1.02 }}
          transition={{ type: "spring", stiffness: 400, damping: 17 }}
          className="relative group"
        >
          <div className="absolute -inset-[1px] bg-gradient-to-br from-indigo-500/20 to-purple-500/20 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div className="relative bg-white/[0.02] rounded-2xl p-6 border border-white/5 backdrop-blur-xl">
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-gradient-to-br from-indigo-500 to-purple-600 p-2.5 rounded-lg">
                <Sparkles className="size-4 text-white" strokeWidth={2.5} />
              </div>
              <h3 className="text-sm text-white/90">AI Intelligence</h3>
            </div>
            <p className="text-xs text-white/50 leading-relaxed">
              Advanced analysis with actionable insights and recommendations
            </p>
          </div>
        </motion.div>

        <motion.div
          whileHover={{ y: -4, scale: 1.02 }}
          transition={{ type: "spring", stiffness: 400, damping: 17 }}
          className="relative group"
        >
          <div className="absolute -inset-[1px] bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div className="relative bg-white/[0.02] rounded-2xl p-6 border border-white/5 backdrop-blur-xl">
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-gradient-to-br from-purple-500 to-pink-600 p-2.5 rounded-lg">
                <svg className="size-4 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={2.5}>
                  <path
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                  />
                </svg>
              </div>
              <h3 className="text-sm text-white/90">Visual Reports</h3>
            </div>
            <p className="text-xs text-white/50 leading-relaxed">
              Beautiful charts and comprehensive data visualizations
            </p>
          </div>
        </motion.div>

        <motion.div
          whileHover={{ y: -4, scale: 1.02 }}
          transition={{ type: "spring", stiffness: 400, damping: 17 }}
          className="relative group"
        >
          <div className="absolute -inset-[1px] bg-gradient-to-br from-pink-500/20 to-rose-500/20 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div className="relative bg-white/[0.02] rounded-2xl p-6 border border-white/5 backdrop-blur-xl">
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-gradient-to-br from-pink-500 to-rose-600 p-2.5 rounded-lg">
                <svg className="size-4 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={2.5}>
                  <path
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
              </div>
              <h3 className="text-sm text-white/90">Lightning Fast</h3>
            </div>
            <p className="text-xs text-white/50 leading-relaxed">
              Process complex documents in seconds with AI acceleration
            </p>
          </div>
        </motion.div>
      </motion.div>
    </motion.div>
  );
}
