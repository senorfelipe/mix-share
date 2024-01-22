import "./App.css";

import { ChakraProvider } from "@chakra-ui/react";
import { Login } from "./pages/Login";

function App() {
  return (
    <>
      <ChakraProvider>
        <Login></Login>
      </ChakraProvider>
    </>
  );
}

export default App;
