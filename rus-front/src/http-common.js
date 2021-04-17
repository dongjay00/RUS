import axios from 'axios';

export default axios.create({
    // baseURL: "http://localhost:8080",
    baseURL: "https://j4b102.p.ssafy.io/api/v1",
    headers: {
        "Content-type": "application/json"
    }
});