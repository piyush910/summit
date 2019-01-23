var express = require('express');
var spawn = require("child_process").spawn; 
global.ipdata;

/* GET home page. */
exports.index = function(req,res,next){
	res.render('index',{title:"SumIT"})
}
exports.sendtosummarize = function(req, res, next) {
	//Validate that the input field is not empty.
   req.checkBody('textInp','Input required').isnotEqual("Enter text to summarise...");
   //Sanitize (trim and escape) the name field.
	 //req.checkBody('textInp').trim().escape();
   
   const errors = req.validationErrors();
    //console.log(errors);
  if (errors) {
	console.log(errors);
	res.send("Error");
	//res.render('index', {errors: errors.array()});
    return;
  } 
  else
  {
	ipdata=req.body.textInp;
	console.log(ipdata);
	
    var spawn = require("child_process").spawn; 
	
	// Parameters passed in spawn - 
	// 1. type_of_script 
	// 2. list containing Path of the script 
	// and arguments for the script 
	
	var process = spawn('python',["./servercode/Summarize-TfIdf.py",req.body.textInp]); 

	// Takes stdout data from script which executed 
	// with arguments and send this data to res object 

	process.stdout.on('data', function(data) { 
		res.render('newoutputview',{ipmessage:ipdata,opmessage:data})
		//res.send(data.toString()); 
	} ) 
}

};

exports.op= function(req,res,next){
	res.render('newoutputview')
}

