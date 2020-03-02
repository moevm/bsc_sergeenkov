import React, {useState, useEffect} from "react";
import AnswersList from './AnswersList';
import './MainInput.css'

export default function MainInput() {
    const ANSWERS = [
        {
            id: 0,
            username: "Konstantin Fokin",
            url: 'stepik.com/kek',
            text: 'танки топ танки топ танки топ танки топ танки топ танки топ танки топ танки топ танки топ танки топ',
            avatar: require('./../assets/avatar.jpg')
        },
        {
            id: 1,
            username: "Konstantin Fokin",
            url: 'stepik.com/kek',
            text: 'танки не топ',
            avatar: require('./../assets/avatar.jpg')
        },
    ];


    const [value, setValue] = useState(null);
    const [answers, setAnswers] = useState([]);
    const [isClicked, setIsClicked] = useState(false);
    const onChange = (e) => {
        setValue(e.target.value);
        setIsClicked(false);
    };
    useEffect(() => {
        async function fetchData() {
            const res = await fetch("https://jsonplaceholder.typicode.com/users");
            res
                .json()
                .then(res => setAnswers(res))
        }

        fetchData();
    });
    return (
        <div className="main-input">
            <div className="main-input__input">
                <input type="text" onChange={onChange}/>
                <button onClick={event => setIsClicked(true)}>Спросить</button>

            </div>
            {(value != null && value !== "" && isClicked) ? (
                    <AnswersList answers={answers}/>) :
                null
            }
        </div>

    )
}