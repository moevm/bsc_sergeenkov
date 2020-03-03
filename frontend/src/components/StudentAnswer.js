import React from "react";
import './StudentAnswer.css'


export default function StudentAnswer(props) {
    return(
        <div className="student-answer">
            <div>
                <p>{props.title}</p>
                {/* <a href={props.url}>Ссылка на Stepik.org</a> */}
            </div>
            <div>
                {/* <p>{props.username}</p> */}
                {/* <img src={props.avatar} alt=""/> */}
            </div>
        </div>
    )
}