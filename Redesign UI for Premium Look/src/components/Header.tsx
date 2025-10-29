import { motion } from "motion/react";
import { FileText, Plus, X } from "lucide-react";
import { Button } from "./ui/button";

export function Header() {
  return (
    <motion.header 
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
      className="border-b border-white/5 bg-[#0A0A0F]/80 backdrop-blur-2xl sticky top-0 z-50"
    >
      <div className="px-8 py-5 flex items-center justify-between max-w-[1800px] mx-auto">
        <div className="flex items-center gap-12">
          <motion.div 
            className="flex items-center gap-3"
            whileHover={{ scale: 1.02 }}
            transition={{ type: "spring", stiffness: 400, damping: 17 }}
          >
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 rounded-lg blur-md opacity-75"></div>
              <div className="relative bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 p-2.5 rounded-lg">
                <FileText className="size-5 text-white" strokeWidth={2.5} />
              </div>
            </div>
            <div>
              <h1 className="text-lg tracking-tight text-white/95">Document Analyzer</h1>
              <p className="text-[11px] text-white/40 tracking-wide uppercase">AI-Powered Intelligence</p>
            </div>
          </motion.div>
        </div>

        <div className="flex items-center gap-3">
          <Button className="gap-2 bg-white text-[#0A0A0F] hover:bg-white/90 h-10 px-5 rounded-lg shadow-lg shadow-white/10 transition-all duration-300 hover:shadow-xl hover:shadow-white/20 group relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
            <Plus className="size-4" strokeWidth={2.5} />
            <span className="text-sm">New Document</span>
          </Button>

          <Button 
            variant="ghost" 
            size="icon" 
            className="hover:bg-white/5 text-white/40 hover:text-white/70 transition-all duration-300 rounded-lg size-10"
          >
            <X className="size-5" strokeWidth={2} />
          </Button>
        </div>
      </div>
    </motion.header>
  );
}
