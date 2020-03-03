import React, {useState, useEffect} from "react";
import AnswersList from './AnswersList';
import './MainInput.css'
import axios from 'axios';

const axiosInstance = axios.create({
    headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
    }
});


export default function MainInput() {
    const [value, setValue] = useState(null);
    const [answers, setAnswers] = useState([]);
    const [isClicked, setIsClicked] = useState(false);
    const onChange = (e) => {
        setValue(e.target.value);
        // setIsClicked(false);
    };
    const onClick = (e) => {
        async function fetchData() {
            const res = await axios.post("http://127.0.01:8000/api/search-similar-questions", {
                question: value
            }, {crossDomain: true});
            setAnswers(res.data);
        }
    
        fetchData();
    };

    return (
        <div className="main-input">
            <div className="main-input__input">
                <input type="text" onChange={onChange}/>
                <button onClick={onClick}>Спросить</button>

            </div>
            <AnswersList answers={answers}/>
        </div>

    )
}