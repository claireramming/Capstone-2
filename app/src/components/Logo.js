import React from 'react'
import logo from '../misc/cr_logo.png'

function Logo() {
    return (
        <a href='https://claireramming.github.io'
            target="_blank" 
            rel="noreferrer noopener">
            <img className='logo' src={logo} alt='logo' />
        </a>
    )
}
export default Logo