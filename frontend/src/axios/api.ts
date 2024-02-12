import axios, { AxiosInstance } from "axios";
import { API_URL } from "../utils/constants";

export class Api {

    private static instance: AxiosInstance | null = null;

    private constructor() { }

    static getInstance(): AxiosInstance {
        if (!Api.instance) {
            Api.instance = Api.createInstance()
        }
        return Api.instance;
    }

    private static createInstance(): AxiosInstance {
        return axios.create({
            baseURL: API_URL,
            withCredentials: true,
            headers: { "Content-Type": "application/json" }
        });
    }

    static renewInstance(): AxiosInstance {
        Api.instance = Api.createInstance();
        return Api.instance
    }
}