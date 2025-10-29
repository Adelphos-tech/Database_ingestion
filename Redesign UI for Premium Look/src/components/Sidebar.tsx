import { motion } from "motion/react";
import { Sparkles, TrendingUp, FileText, Clock, ArrowUpRight, Send, ChevronDown } from "lucide-react";
import { Button } from "./ui/button";
import { ScrollArea } from "./ui/scroll-area";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: {
    opacity: 1,
    x: 0,
    transition: {
      type: "spring",
      stiffness: 100,
      damping: 15,
    },
  },
};

export function Sidebar() {
  return (
    <aside className="w-96 border-r border-white/5 bg-[#0A0A0F]/40 backdrop-blur-xl flex flex-col h-full">
      <ScrollArea className="flex-1 overflow-auto">
        <motion.div 
          className="p-8 space-y-8 pb-4"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Status */}
          <motion.div variants={itemVariants}>
            <div className="flex items-center gap-2 mb-6">
              <div className="size-1.5 rounded-full bg-indigo-400 animate-pulse"></div>
              <span className="text-[10px] tracking-widest text-white/30 uppercase">
                Active Analysis
              </span>
            </div>

            <div className="relative group">
              <div className="absolute -inset-[1px] bg-gradient-to-br from-indigo-500/20 via-purple-500/20 to-pink-500/20 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative bg-gradient-to-br from-white/[0.03] to-white/[0.01] rounded-2xl p-6 border border-white/5 backdrop-blur-xl">
                <p className="text-sm text-white/60 leading-relaxed">
                  Upload a document to begin AI-powered analysis. Get insights, trends, and 
                  visualizations in seconds.
                </p>
              </div>
            </div>
          </motion.div>

          {/* Capabilities */}
          <motion.div variants={itemVariants} className="space-y-3">
            <p className="text-[10px] tracking-widest text-white/30 uppercase mb-4">Capabilities</p>
            
            <motion.div
              whileHover={{ x: 4, scale: 1.01 }}
              transition={{ type: "spring", stiffness: 400, damping: 17 }}
              className="flex items-center gap-4 p-4 rounded-xl bg-white/[0.02] border border-white/5 hover:border-white/10 hover:bg-white/[0.04] transition-all duration-300 cursor-pointer group"
            >
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg blur-md opacity-50 group-hover:opacity-75 transition-opacity"></div>
                <div className="relative bg-gradient-to-br from-indigo-500 to-purple-600 p-2.5 rounded-lg">
                  <TrendingUp className="size-4 text-white" strokeWidth={2.5} />
                </div>
              </div>
              <div className="flex-1">
                <p className="text-sm text-white/90 mb-0.5">Trend Analysis</p>
                <p className="text-xs text-white/40">Pattern recognition</p>
              </div>
              <ArrowUpRight className="size-4 text-white/20 group-hover:text-white/40 transition-colors" />
            </motion.div>

            <motion.div
              whileHover={{ x: 4, scale: 1.01 }}
              transition={{ type: "spring", stiffness: 400, damping: 17 }}
              className="flex items-center gap-4 p-4 rounded-xl bg-white/[0.02] border border-white/5 hover:border-white/10 hover:bg-white/[0.04] transition-all duration-300 cursor-pointer group"
            >
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-purple-500 to-pink-600 rounded-lg blur-md opacity-50 group-hover:opacity-75 transition-opacity"></div>
                <div className="relative bg-gradient-to-br from-purple-500 to-pink-600 p-2.5 rounded-lg">
                  <FileText className="size-4 text-white" strokeWidth={2.5} />
                </div>
              </div>
              <div className="flex-1">
                <p className="text-sm text-white/90 mb-0.5">Smart Summaries</p>
                <p className="text-xs text-white/40">Key insights extraction</p>
              </div>
              <ArrowUpRight className="size-4 text-white/20 group-hover:text-white/40 transition-colors" />
            </motion.div>

            <motion.div
              whileHover={{ x: 4, scale: 1.01 }}
              transition={{ type: "spring", stiffness: 400, damping: 17 }}
              className="flex items-center gap-4 p-4 rounded-xl bg-white/[0.02] border border-white/5 hover:border-white/10 hover:bg-white/[0.04] transition-all duration-300 cursor-pointer group"
            >
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-pink-500 to-rose-600 rounded-lg blur-md opacity-50 group-hover:opacity-75 transition-opacity"></div>
                <div className="relative bg-gradient-to-br from-pink-500 to-rose-600 p-2.5 rounded-lg">
                  <Clock className="size-4 text-white" strokeWidth={2.5} />
                </div>
              </div>
              <div className="flex-1">
                <p className="text-sm text-white/90 mb-0.5">Real-time Processing</p>
                <p className="text-xs text-white/40">Instant analysis</p>
              </div>
              <ArrowUpRight className="size-4 text-white/20 group-hover:text-white/40 transition-colors" />
            </motion.div>
          </motion.div>

          {/* Statistics */}
          <motion.div variants={itemVariants} className="grid grid-cols-2 gap-4">
            <div className="relative group">
              <div className="absolute -inset-[1px] bg-gradient-to-br from-indigo-500/20 to-purple-500/20 rounded-xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative bg-white/[0.02] rounded-xl p-5 border border-white/5 backdrop-blur-xl">
                <p className="text-3xl mb-1 bg-gradient-to-br from-indigo-400 to-purple-400 bg-clip-text text-transparent tracking-tight">
                  127
                </p>
                <p className="text-[10px] text-white/40 uppercase tracking-wider">Documents</p>
              </div>
            </div>
            <div className="relative group">
              <div className="absolute -inset-[1px] bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative bg-white/[0.02] rounded-xl p-5 border border-white/5 backdrop-blur-xl">
                <p className="text-3xl mb-1 bg-gradient-to-br from-purple-400 to-pink-400 bg-clip-text text-transparent tracking-tight">
                  98%
                </p>
                <p className="text-[10px] text-white/40 uppercase tracking-wider">Accuracy</p>
              </div>
            </div>
          </motion.div>

        </motion.div>
      </ScrollArea>

      {/* Chat Interface */}
      <div className="p-8 pt-4 space-y-4 border-t border-white/5">
        <p className="text-[10px] tracking-widest text-white/30 uppercase">Ask Questions</p>
        
        {/* Chat Input with Buttons */}
        <div className="relative group">
          <div className="absolute -inset-[1px] bg-gradient-to-br from-indigo-500/0 to-purple-500/0 group-focus-within:from-indigo-500/30 group-focus-within:to-purple-500/30 rounded-xl blur transition-all duration-500"></div>
          <div className="relative flex items-center gap-2 bg-white/[0.02] border border-white/5 group-focus-within:border-white/20 rounded-xl p-2 backdrop-blur-xl transition-all duration-300">
            <input
              type="text"
              placeholder="Type your question..."
              className="flex-1 bg-transparent outline-none px-2 py-2 text-sm text-white/90 placeholder:text-white/30"
            />
            
            {/* Model Selector Button */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button 
                  variant="ghost" 
                  size="icon"
                  className="gap-1 text-white/60 hover:text-white/90 hover:bg-white/5 border border-white/5 h-9 w-9 rounded-lg backdrop-blur-xl transition-all duration-300 shrink-0"
                >
                  <div className="size-1.5 rounded-full bg-indigo-400 animate-pulse"></div>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent 
                align="end" 
                className="w-60 bg-[#16161F]/95 backdrop-blur-2xl border-white/10 shadow-2xl"
              >
                <DropdownMenuItem className="text-white/70 hover:text-white hover:bg-white/5 focus:bg-white/5 focus:text-white">
                  <div className="size-1.5 rounded-full bg-indigo-400 mr-2"></div>
                  Gemini 2.5 Flash
                  <span className="ml-auto text-[10px] text-white/40 uppercase tracking-wider">Current</span>
                </DropdownMenuItem>
                <DropdownMenuItem className="text-white/70 hover:text-white hover:bg-white/5 focus:bg-white/5 focus:text-white">
                  <div className="size-1.5 rounded-full bg-purple-400 mr-2"></div>
                  Gemini 2.0 Ultra
                </DropdownMenuItem>
                <DropdownMenuItem className="text-white/70 hover:text-white hover:bg-white/5 focus:bg-white/5 focus:text-white">
                  <div className="size-1.5 rounded-full bg-pink-400 mr-2"></div>
                  GPT-4 Turbo
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Send Button */}
            <Button 
              size="icon"
              className="gap-2 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 hover:from-indigo-600 hover:via-purple-600 hover:to-pink-600 text-white h-9 w-9 rounded-lg shadow-lg shadow-indigo-500/25 transition-all duration-300 hover:shadow-indigo-500/40 hover:scale-[1.05] group/send relative overflow-hidden shrink-0"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover/send:translate-x-[100%] transition-transform duration-1000"></div>
              <Send className="size-4" strokeWidth={2.5} />
            </Button>
          </div>
        </div>
      </div>
    </aside>
  );
}
