import axios from "axios";
import { push } from "connected-react-router";

export const addBoast = ({message}) => (dispatch) => {
    axios({
        method: "POST",
        url: "https://localhost:8000/apiBaRs/",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ boasts: message })
    })
    .then(() => {
        dispatch(push("/"));
    })
    .catch(err => console.log(err))
}

export const addRoast = ({message}) => (dispatch) => {
    axios({
        method: "POST",
        url: "https://localhost:8000/apiBaRs/",
        headers: {"Content-Type": "application/json"},
        data: {roasts: message}
    })
    .then(() => {
        dispatch(push("/"));
    })
    .catch(err => console.log(err))
}