import axios from "axios";
import { createContext, useContext, useMemo, useState } from "react";
import { API } from "../api";

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
    API.interceptors.response.use(
      (response) => response,
      async (response) => {
        const originalRequest = response.config;

        if (response.response.status === 401 && !originalRequest._retry) {
          console.log(JSON.stringify(originalRequest));
          console.log("token timed out");
          originalRequest._retry = true;

          try {
            const response = await API.post("/user/token/refresh", {});
            console.log("new token obtained: " + response.data);

            const token = response.data["access"];
            setToken(token);

            // Retry the original request with the new token
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return axios(originalRequest);
          } catch (error) {
            console.log("token error");
            // Handle refresh token error or redirect to login
          }
        }
        // TODO: add handling for expired refresh token
        return Promise.reject(response);
      }
    );
  }, []);

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
