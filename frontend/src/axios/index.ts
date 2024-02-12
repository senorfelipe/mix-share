import axios, { AxiosRequestConfig } from "axios";
import { useEffect, useState } from "react";
import { Api } from "./api";


export const API = Api.getInstance();


export const useApi = (params: AxiosRequestConfig<unknown>) => {
    const [loading, setLoading] = useState(true)
    const [data, setData] = useState<unknown>(null);
    const [error, setError] = useState<unknown>(null);

    const fetchData = async (): Promise<void> => {
        try {
            const response = await API.request(params);
            setData(response.data);
        }
        catch (error) {
            if (axios.isAxiosError(error)) {
                setError("axios error with message: " + error.message);
            } else {
                setError(error);
            }
            setLoading(false);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        console.log("fetch api: " + JSON.stringify(params));
        fetchData();
    }, []);

    return { loading, data, error, fetchData }
};
