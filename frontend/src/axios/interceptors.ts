import { AxiosError, isAxiosError } from "axios";
import { useEffect, useState } from "react";
import { API } from ".";
import { useAuth } from "../service/AuthProvider";
import { API_URL } from "../utils/constants";

const AxiosInterceptor = ({ children }) => {

    const [isInitialized, setIsInitialized] = useState(false);
    const { setToken } = useAuth()

    useEffect(() => {
        console.log("interceptors useEffect")
        const isUnauthorizedError = (error: AxiosError) => {
            return error.config && error.response?.status === 401;
        }

        const refreshToken = async () => {
            console.log("trying refresh");
            return API.post(API_URL + "/user/token/refresh");
        }

        async function authInterceptor(error) {
            console.log("repsonse error");
            const originalRequest = error.config;
            console.log(JSON.stringify(originalRequest))

            if (isUnauthorizedError(error) && originalRequest.url !== API_URL + "/user/token/refresh" && !originalRequest._retry) {
                try {
                    originalRequest._retry = true;
                    const response = await refreshToken();
                    console.log("refresh token response")
                    const token = response.data["access"];
                    setToken(token);
                    originalRequest.headers["Authorization"] = "Bearer " + token;
                    return API(originalRequest); // retries the original request
                } catch (refreshError) {
                    if (isAxiosError(error)) {
                        if (isUnauthorizedError(error)) {
                            console.log("refresh error");
                            console.log(JSON.stringify(error));
                            setToken();
                            // window.location.replace("/login");
                        }
                    }
                }
            }
            return Promise.reject(error);
        }
        console.log("axios interceptor added");
        API.interceptors.response.use(
            (response) => response, authInterceptor);

        setIsInitialized(true)

    }, []);

    return isInitialized && children

}

export { AxiosInterceptor };
