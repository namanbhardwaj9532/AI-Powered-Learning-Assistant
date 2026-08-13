import Login from "./components/login"
import Registration from "./components/Registration";
import Index from "./components/index";
import Main from "./components/main";
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
      </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;