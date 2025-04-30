import HomePage from "../pages/Homepage";
import { Route, Routes } from "react-router-dom";

const RoutesPath = () => {
  return (
    <>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="*" element={<HomePage />} />
      </Routes>
    </>
  );
};

export default RoutesPath;
