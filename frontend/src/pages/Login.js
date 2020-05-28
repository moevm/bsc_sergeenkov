import React, { useEffect, useContext, useState } from 'react'
import SearchContext from '../context/SearchContext'

export default function Login(props) {
    const search = useContext(SearchContext)
    const redirectUrl = process.env.REDIRECT_URL || 'https://bsc-sergeenkov.rc.robotbull.com/redirect'
    const [clicked, setClicked] = useState(false)
    return (
        <div className="login">
        </div>
    )
}
