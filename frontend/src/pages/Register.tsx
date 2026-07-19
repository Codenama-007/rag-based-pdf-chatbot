import { Button } from "@/components/ui/button"
import { useState } from "react";
import { Link } from "react-router-dom"
import { toast } from "sonner";
import { useNavigate } from "react-router-dom";


const Register = () => {
    const navigate = useNavigate()
    interface RegisterData{
        username : string ;
        email : string ;
        password : string
    }
    const [Data, setData] = useState<RegisterData>({
        username : "" ,
        email : "" ,
        password : ""
    })

    const register_function = async(e :React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        // console.log(Data)
        const response = await fetch('http://127.0.0.1:8000/register' , {
            method : "POST" ,
            headers : {
                "Content-type" : "application/json"
            } ,
            body : JSON.stringify(Data)
        }
        )
        const response_from_server = await response.json()
        if (!response.ok)
        {
            return (
                toast.error(`${response_from_server.detail}` , {position : "bottom-center"})
            )
        }
        else{
            toast.success("User Registered Successfully" , {position : "bottom-center"})
            navigate("/")
            // console.log(response_from_server)
            
        }
        }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
        <div className="p-4 rounded-xl shadow-md">
            <h1 className="text-center text-2xl font-bold">Register</h1>
            <form className="space-y-4" onSubmit = {register_function}>
                <input type="text" name="username" className = "shadow-md rounded-xl w-full p-4 border-none outline-none mt-2.5" placeholder="Enter Your Username" value={Data.username} onChange={(e) => {setData({...Data , username:e.target.value})}} required/>

                <input type="email" name="email" className = "shadow-md rounded-xl w-full p-4 border-none outline-none mt-2.5" placeholder="Enter Your Email" value={Data.email} onChange={(e) => {setData({...Data , email:e.target.value})}} required/>

                <input type="password" name="" className = "shadow-md rounded-xl w-full p-4 border-none outline-none mt-2.5" placeholder="Enter Your Password" value={Data.password} onChange={(e) => {setData({...Data , password : e.target.value})}} required/>

                <Button size={'lg'} type="submit" className="bg-white text-black shadow-md hover:bg-black hover:text-white mx-auto block w-80 mt-2.5 mb-2.5">Register</Button>
            </form>
            <p className="text-center mt-4">
                Already have an Account  <Link to = {'/'} className="underline">Click Here</Link>
            </p>
            

        </div>
        
    </div>
  )
}

export default Register