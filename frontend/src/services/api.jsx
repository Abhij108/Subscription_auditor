import axios from "axios";


const API = axios.create({
    baseURL: "http://127.0.0.1:8000/api"
});


export async function analyzeCSV(file) {

    const formData = new FormData();

    formData.append(
        "file",
        file
    );

    const response = await API.post(
        "/analyze/",
        formData
    );

    return response.data;
}