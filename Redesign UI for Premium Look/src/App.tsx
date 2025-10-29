import { Background3D } from "./components/Background3D";
import { Header } from "./components/Header";
import { Sidebar } from "./components/Sidebar";
import { FileUpload } from "./components/FileUpload";

export default function App() {
  return (
    <div className="size-full flex flex-col bg-[#0A0A0F] relative overflow-hidden">
      {/* 3D Background */}
      <Background3D />
      
      {/* Gradient Overlays */}
      <div className="fixed inset-0 bg-gradient-to-br from-indigo-500/5 via-purple-500/5 to-pink-500/5 pointer-events-none"></div>
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/10 via-transparent to-transparent pointer-events-none"></div>
      
      <Header />
      <div className="flex-1 flex overflow-hidden relative z-10">
        <Sidebar />
        <main className="flex-1 overflow-auto">
          <div className="container mx-auto px-12 py-16 max-w-[1400px]">
            <FileUpload />
          </div>
        </main>
      </div>
    </div>
  );
}
