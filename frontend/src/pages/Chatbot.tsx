import { SidebarProvider} from "@/components/ui/sidebar";
import Side_bar from "../components/Side_bar";
import Pdf_Reader from "../components/Pdf_Reader";

const Chatbot = () => {
  return (
    <SidebarProvider>
      <div className="w-full flex items-center justify-between min-h-screen gap-4">
        <Side_bar />
        <main className="flex-1 p-4 min-w-0 ">
          
          <Pdf_Reader/>
        </main>
      </div>
    </SidebarProvider>
  );
};

export default Chatbot;