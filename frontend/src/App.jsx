import Login from "./components/login"
import Registration from "./components/Registration";
import Index from "./components/index";
import Main from "./components/main";
import Notes from "./components/notes";
import File from "./components/file";
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
      </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;