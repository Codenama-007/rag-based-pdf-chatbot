import {Routes , Route} from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Chatbot from "./pages/Chatbot"
import VideoSumarizer from "./pages/VideoSumarizer"
const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Login/>} />
      <Route path="/register" element={<Register/>} />
      <Route path="/main" element={<Chatbot/>} />
      <Route path="/video-summary" element={<VideoSumarizer/>} />

    </Routes>
  )
}

export default App