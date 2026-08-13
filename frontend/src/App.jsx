import Login from "./components/login"
import Registration from "./components/Registration";
import Home from "./components/home";
import { BrowserRouter, Routes, Route } from "react-router-dom";
function App(){

  return (
    <div>
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />}></Route>
        <Route path="/login" element={<Login />}></Route>
        <Route path="/registration" element={<Registration />}></Route>
      </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;