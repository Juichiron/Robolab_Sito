import "./App.css";

import { BrowserRouter } from "react-router-dom";
import RoutesPath from "./RoutesPath/RoutesPath";

const App = () => {
  return (
    <>
      <BrowserRouter
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      >
        <RoutesPath />
      </BrowserRouter>
    </>
  );
};

export default App;
