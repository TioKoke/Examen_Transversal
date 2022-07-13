class Registro{
    rut;
    nombre;
    direccion;
    fono;
    ciudad;
    correo;
    //get y set
    setRut(rut){ this.password=rut;}
    setNombre(nombre){ this.nombre=nombre;}
    setFono(fono){ this.fono=fono;}
    setCiudad(city){ this.ciudad=city;}
    setCorreo(correo){ this.correo=correo;}

    getRut(){ return this.rut;}
    getNombre(){ return this.nombre;}
    getFono(){ return this.fono;}
    getCiudad(){ return this.ciudad;}
    getCorreo(){ return this.correo;}
    
}