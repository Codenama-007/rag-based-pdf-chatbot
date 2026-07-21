import { Button } from "@/components/ui/button"
import { useState } from "react"
import { Link } from "react-router-dom"
import { toast } from "sonner";
import { useNavigate } from "react-router-dom";


const Login = () => {
    const navigate = useNavigate()
    interface Loginform {
        email: string;
        password: string
    }
    const [Data, setData] = useState<Loginform>({
        email: "",
        password: ""
    })
    const login_function = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        console.log(" Login Button Was Clicked ")
        // console.log(Data)
        const response = await fetch(`${import.meta.env.VITE_API_URL}/login`, {
            method: "POST",
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify(Data)
        }
        )
        const data = await response.json();
        if (!response.ok) {
            toast.error(data.detail, {
                position: "bottom-center"
            });
            return;
        }

        localStorage.setItem("token", data.access_token);
        toast.success("Successfully Connected");
        navigate("/main");
    }
    return (

        <div className="min-h-screen flex items-center justify-center p-4">
            <div className="p-4 rounded-xl shadow-md">
                <h1 className="text-center text-black text-2xl font-bold">Login</h1>
                <form className="space-y-4" onSubmit={login_function}>
                    <input type="email" name="email" className="shadow-md rounded-xl w-full p-4 border-none outline-none mt-2.5" placeholder="Enter Your Email" value={Data.email} onChange={(e) => { setData({ ...Data, email: e.target.value }) }} required />

                    <input type="password" name="" className="shadow-md rounded-xl w-full p-4 border-none outline-none mt-2.5" placeholder="Enter Your Password" required value={Data.password} onChange={(e) => { setData({ ...Data, password: e.target.value }) }} />

                    <Button size={'lg'} type="submit" className="bg-white text-black shadow-md hover:bg-black hover:text-white mx-auto block w-80 mt-2.5 mb-2.5" >Login</Button>

                </form>

                <p className="text-center mt-4">
                    New Here <Link to={'/register'} className="underline">Click Here</Link>
                </p>

            </div>

        </div>
    )
}

export default Login