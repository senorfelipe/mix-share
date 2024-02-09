import React from "react";
import ReactDOM from "react-dom/client";

import { ChakraProvider } from "@chakra-ui/react";

import Routes from "./routes";
import AuthProvider from "./service/AuthProvider";
import { AxiosInterceptor } from "./axios/interceptors";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ChakraProvider>
      <AuthProvider>
        <AxiosInterceptor>
          <Routes />
        </AxiosInterceptor>
      </AuthProvider>
    </ChakraProvider>
  </React.StrictMode>
);
