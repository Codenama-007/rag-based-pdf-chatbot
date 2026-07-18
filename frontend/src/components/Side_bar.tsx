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
import { useEffect , useState} from "react";
import { File, LogOut, User, Video } from "lucide-react";

const Side_bar = () => {
  const [username, setusername] = useState("")
  useEffect(() => {
    const getProfile = async () => {
        const token = localStorage.getItem("token");

        const response = await fetch("http://127.0.0.1:8000/profile", {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        const data = await response.json();

        // console.log(data.username);
        setusername(data.username)
    };

    getProfile();
}, []);
  const tools = [
    {
      title: "PDF Chat",
      url: "/main",
      icon: <File size={20} />,
    },
    {
      title: "Video Summarizer",
      url: "/video-summary",
      icon: <Video size={20} />,
    },
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
            <SidebarMenuButton asChild>
              <Link to="/logout">
                <LogOut size={20} />
                <span>Logout</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>

    </Sidebar>

  );
};

export default Side_bar;