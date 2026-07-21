import { SidebarTrigger } from './ui/sidebar'
import { Button } from './ui/button'
import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown'

const Pdf_Reader = () => {
  type Message = {
    role: 'user' | 'assistant' | 'error'
    content: string
  }
  const [file, setFile] = useState<File | null>(null)
  const [disabled, setDisabled] = useState(false)
  const [disabledChat, setDisabledChat] = useState(true)
  const [query, setQuery] = useState("")
  const [messages, setMessages] = useState<Message[]>([])
  const [sending, setSending] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)
  const [documentId, setDocumentId] = useState<number | null>(null)
  // const token = localStorage.getItem("token");

  // Auto-scroll to the latest message whenever the list changes
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages, sending])

  const pdf_chat = async () => {
    if (!file) {
      setMessages(prev => [...prev, { role: 'error', content: 'Please choose a PDF file before uploading.' }])
      return
    }

    setDisabled(true)
    try {
      const token = localStorage.getItem("token")
      const form_data = new FormData()
      form_data.append("pdf", file)
      const response = await fetch(`${import.meta.env.VITE_API_URL}/get-pdf`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`
        },
        body: form_data
      })
      const data = await response.json()
      console.log(data.message)
      if (data.status_code == 200) {
        setDisabledChat(false)
        setDocumentId(data.document_id)
      } else {
        setMessages(prev => [...prev, { role: 'error', content: 'Failed to process the PDF. Please try again.' }])
      }
    } catch (error) {
      console.log(error)
      setMessages(prev => [...prev, { role: 'error', content: 'Something went wrong while uploading the PDF.' }])
    } finally {
      setDisabled(false)
    }
  }

  const chat_with_pdf = async () => {
    if (query.trim() === '') {
      return
    }

    const userMessage = query
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setQuery("")
    setSending(true)

    try {
      const token = localStorage.getItem("token")
      const response = await fetch(`${import.meta.env.VITE_API_URL}/pdf-chat`, {
        method: "POST",
        headers: {
          "Content-type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ query: userMessage, document_id: documentId })
      })

      const data = await response.json()

      if (data.status_code == 200) {
        setMessages(prev => [...prev, { role: 'assistant', content: data.response_from_llm }])
      } else {
        setMessages(prev => [...prev, { role: 'error', content: 'The assistant could not answer that. Please try again.' }])
      }
    } catch (error) {
      console.log(error)
      setMessages(prev => [...prev, { role: 'error', content: 'Something went wrong while contacting the assistant.' }])
    } finally {
      setSending(false)
    }
  }
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !disabledChat && !sending) {
      chat_with_pdf()
    }
  }

  return (
    <div className="min-h-screen flex flex-col gap-4 p-3 sm:p-4 md:p-6 bg-gray-50">
      {/* Heading  */}
      <div className="w-full p-4 sm:p-6 shadow-md rounded-xl bg-white border border-gray-200">
        <div className="flex items-center gap-3">
          <SidebarTrigger />
          <h1 className="text-xl sm:text-2xl md:text-3xl font-bold text-center flex-1">Hello World</h1>
        </div>
      </div>

      {/* PDF chat Component */}
      <div
        ref={scrollRef}
        className="w-full min-h-64 sm:min-h-80 md:min-h-96 max-h-[32rem] bg-white rounded-xl shadow-md border border-gray-200 p-4 sm:p-6 overflow-y-auto flex flex-col gap-3"
      >
        {messages.length === 0 ? (
          <p className="text-gray-400 text-center m-auto">Start by uploading a PDF and asking questions...</p>
        ) : (
          messages.map((msg, index) => {
            if (msg.role === 'error') {
              return (
                <div key={index} className="w-full flex justify-center">
                  <div className="max-w-[85%] sm:max-w-[70%] rounded-lg px-4 py-2 text-sm bg-red-50 text-red-600 border border-red-200">
                    {msg.content}
                  </div>
                </div>
              )
            }

            const isUser = msg.role === 'user'
            return (
              <div key={index} className={`w-full flex ${isUser ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-[85%] sm:max-w-[70%] rounded-2xl px-4 py-2 sm:py-3 shadow-sm break-words ${isUser
                    ? 'bg-blue-600 text-white rounded-br-sm'
                    : 'bg-gray-100 text-gray-800 border border-gray-200 rounded-bl-sm'
                    }`}
                >
                  <ReactMarkdown>
                    {msg.content}
                  </ReactMarkdown>
                </div>
              </div>
            )
          })
        )}

        {/* Typing indicator while waiting for the assistant's response */}
        {sending && (
          <div className="w-full flex justify-start">
            <div className="max-w-[70%] rounded-2xl rounded-bl-sm px-4 py-3 bg-gray-100 border border-gray-200 flex gap-1 items-center">
              <span className="w-2 h-2 rounded-full bg-gray-400 animate-bounce [animation-delay:-0.3s]"></span>
              <span className="w-2 h-2 rounded-full bg-gray-400 animate-bounce [animation-delay:-0.15s]"></span>
              <span className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"></span>
            </div>
          </div>
        )}
      </div>

      {/* Pdf Input section Component */}
      <div className="w-full space-y-4">

        {/* File Upload Section */}
        <div className="w-full bg-white rounded-xl shadow-md border border-gray-200 p-4 sm:p-6">
          <div className='file-provider flex flex-col sm:flex-row gap-2 sm:gap-3 items-stretch sm:items-center'>
            <input
              type="file"
              accept='.pdf'
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  setFile(e.target.files[0])
                }
              }}
              className='...'
            />
            <Button
              className='w-full sm:w-auto px-6 sm:px-8 py-2 sm:py-2 rounded-lg hover:bg-white hover:text-black shadow-md bg-blue-600 text-white font-semibold transition-colors disabled:opacity-50'
              onClick={pdf_chat}
              disabled={disabled}
            >
              {disabled ? 'Uploading...' : 'Upload File'}
            </Button>
          </div>
        </div>

        {/* Separator / Chat Input Section */}
        <div className="w-full bg-white rounded-xl shadow-md border border-gray-200 p-4 flex-wrap sm:p-6">
          <div className='flex flex-col sm:flex-row gap-2 sm:gap-3 items-stretch sm:items-center'>
            <input
              type="text"
              placeholder='Enter Your Question'
              className='flex-1 p-3 sm:p-4 rounded-lg shadow-md border border-gray-300 outline-none focus:ring-2 focus:ring-green-500 text-sm disabled:opacity-50 disabled:bg-gray-100'
              value={query}
              onChange={(e) => { setQuery(e.target.value) }}
              onKeyDown={handleKeyDown}
              disabled={disabledChat}
            />
            <Button
              className='w-full sm:w-auto px-6 sm:px-8 py-2 sm:py-2 rounded-lg hover:bg-white hover:text-black shadow-md bg-green-600 text-white font-semibold transition-colors disabled:opacity-50'
              onClick={chat_with_pdf}
              disabled={disabledChat || sending}
            >
              {sending ? 'Sending...' : 'Send'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Pdf_Reader;