var express = require('express');
var router = express.Router();
var homeRouter = require('./routes/sample');
/* GET home page. */
router.get('/', homeRouter.index);
router.post('/',homeRouter.sendtosummarize);
router.get('/output',homeRouter.op);
module.exports = router;
