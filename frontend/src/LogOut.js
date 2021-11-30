import { Navigate } from 'react-router-dom'

function LogOut() {
    localStorage.removeItem('User')
    return <Navigate to="Home"/>
}

export default LogOut