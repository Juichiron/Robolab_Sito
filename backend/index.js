//! Come DBMS usare STRAPI
//! Login Vedi progetto ingegneria
//! Utilizza session storage

const express=require("express")
const mysql=require("mysql")
const cors=require("cors")
const server=express()
const port=3000


//Crea endpoint registra

//Crea endpoint login utente e admin

//Crea endpoint prenotaTicket con riferimento al lo script python

//Crea fuzione Logout

//Prevedi annullaPrenotazione

//? se avanza tempo vedi di implenetare anche viusualizzazione grafico di numero di ticket prenotati per ogni evento

server.post("/generateTicktet",(req,res)=>{
    const {eventId, userId}=req.body
    console.log(eventId,userId)
    //? Qui ci va la chiamata al python per generare il ticket
    //? Esempio di chiamata al python
    //? const {PythonShell}=require("python-shell")
    //? PythonShell.run("script.py",null,(err,result)=>{
    //?     if(err) throw err
    //?     console.log(result)
    //? })
    res.send("Ticket generato")
})

//? Utilizza NicolAI?
server.listen(port,()=>{
    console.log(`Server in ascolto sulla porta ${port}`)
    console.log(`http://localhost:${port}`)
});