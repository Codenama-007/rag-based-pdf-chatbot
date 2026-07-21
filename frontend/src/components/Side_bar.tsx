import { Link } from "react-router-dom";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem
} from "./ui/sidebar";
import { useEffect, useState } from "react";
import { File, LogOut, User} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";



const Side_bar = () => {
  
  const navigate = useNavigate()
  const [username, setusername] = useState("")

  // modified by claude 
  useEffect(() => {
    const getProfile = async () => {
      const token = localStorage.getItem("token");
      const response = await fetch(`${import.meta.env.VITE_API_URL}/profile`, {
        method: "GET",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) {
        navigate('/');
        return;
      }

      const data = await response.json();
      setusername(data.username);
    };

    getProfile();
  }, []);
  const handleLogout = () => {
  localStorage.removeItem("token")
  toast.info("successfully Logout " , {position : "bottom-center"})
  
  navigate('/')
}
  const tools = [
    {
      title: "PDF Chat",
      url: "/main",
      icon: <File size={20} />,
    }
  ];

  return (

    <Sidebar collapsible="icon">

      {/* Header */}
      <SidebarHeader>
        <h1 className="text-center text-2xl font-bold">
          My App
        </h1>
      </SidebarHeader>

      {/* Main Menu */}
      <SidebarContent>
        <SidebarMenu>
          {tools.map((tool) => (
            <SidebarMenuItem
              key={tool.title}
              className="shadow-md hover:shadow-lg transition-shadow duration-300"
            >
              <SidebarMenuButton asChild>
                <Link to={tool.url}>
                  {tool.icon}
                  <span>{tool.title}</span>
                </Link>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarContent>

      {/* Bottom Section */}
      <SidebarFooter className="border-t">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild>
              <Link to="/profile">
                <User size={20} />
                <span>{username}</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton onClick={handleLogout}>
              <LogOut size={20} />
              <span>Logout</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>

    </Sidebar>

  );
};

export default Side_bar;