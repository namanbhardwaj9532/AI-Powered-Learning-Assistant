import Login from "./components/login"
import Registration from "./components/Registration";
import Index from "./components/index";
import Main from "./components/main";
import Notes from "./components/notes";
import Chatbot from "./components/chatbot";
import File from "./components/file";
import Test from "./components/test"
import Flashcards from "./components/flashcards";
import Contest from "./components/Contest";
import Testpage from "./components/testpage";
import { BrowserRouter, Routes, Route } from "react-router-dom";
function App(){

  return (
    <div>
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<Index />}></Route>
        <Route path="/login" element={<Login />}></Route>
        <Route path="/registration" element={<Registration />}></Route>
        <Route path="/main" element={<Main />}></Route>
        <Route path="/notes" element={<Notes />}></Route>
        <Route path="/file/:note_id" element={<File />}></Route>
        <Route path="/chatbot" element={<Chatbot />}></Route>
        <Route path="/test/:note_id" element={<Test />}></Route>
        <Route path="/flashcards/:note_id" element={<Flashcards />}></Route>
        <Route path="/contest/:note_id" element={<Contest />}></Route>
        <Route path="/testpage" element={<Testpage />}></Route>
      </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;