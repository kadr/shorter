import axios from 'axios';
const session = 'sdjfnhkajhdfas7687sdafasd'
const API_URL = 'http://localhost'


export default class UrlsService {
    constructor(){}

    getAllUrls() {
       return  axios.get(`${API_URL}/api/url`, {
            params: {
                session: session,
                format: 'json',
            }
        })
            .then(response =>  response.data)
            .catch(error => console.log("error ", error))
    }
    getUrl(pk) {
        return axios.get(`${API_URL}/api/url/${pk}`, {
            params: {
                format: 'json',
            }
        })
            .then(response => response.data)
            .catch(error => console.log("error ", error))
    }
    createUrl(link) {
       return axios.post(`${API_URL}/api/url/`, {
            params: {
                format: 'json',
                session: '',
                full: link
            }
        })
            .then(response =>  response.data)
            .catch(error => console.log("error ", error))
    }
}