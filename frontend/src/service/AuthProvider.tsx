import { createContext, useContext, useMemo, useState } from "react";
import { API } from "../axios";

interface JWTTokenType {
  token: string | null;
  setToken: (newToken: string) => void;
}

const AuthContext = createContext<JWTTokenType | null>(null);

const AuthProvider = ({ children }) => {
  const [token, setToken_] = useState(localStorage.getItem("access_token"));

  const setToken = (new_token: string) => {
    setToken_(new_token);
  };

  useMemo(() => {
    if (token) {
      console.log("updating access token");
      API.defaults.headers.common["Authorization"] = "Bearer " + token;
      localStorage.setItem("access_token", token);
    } else {
      delete API.defaults.headers.common["Authorization"];
      localStorage.removeItem("access_token");
    }
  }, [token]);

  const contextValue = useMemo(
    () => ({
      token,
      setToken,
    }),
    [token]
  );

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};

export default AuthProvider;
