<template>
  <div class="login">
    <div class="bg">
    </div>
    <Modal class="login-modal" v-model="loginModal" width="360" :closable="false" :mask-closable="false">
      <div>
        <h2 style="margin:10px;color:#abcdef;text-align:center">
          <img :src="require('@/assets/qizhi.png')" alt="" height="50">
        </h2>
        <Form ref="formValidate" :model="formValidate" :rules="ruleValidate">
          <Form-item prop="name">
            <Input v-model="formValidate.username" placeholder="请输入姓名"></Input>
          </Form-item>
          <Form-item prop="password">
            <Input v-model="formValidate.password" @keyup.native.enter="handleSubmit('formValidate')" type="password" placeholder="请输入密码"></Input>
          </Form-item>

          <Row>
            <Col span="12">
              <Checkbox-group v-model="formValidate.remember">
                <Checkbox label="记住我"></Checkbox>
              </Checkbox-group>
            </Col>
<!--            <Col span="12">
              <a style="float:right" @click="toRegister">新用户注册</a>
            </Col>-->
          </Row>

        </Form>
      </div>
      <div slot="footer">
        <Button type="primary" size="large" long :loading="modal_loading" @click="handleSubmit()">登录
        </Button>
        <small style="text-align: center;display:block" class="subText">©copyright by Nelvt</small>
      </div>
    </Modal>
  </div>
</template>
<script>

  import Cookies from 'js-cookie'
  export default {
    name: 'login',
    data () {
      return {
        loginModal: true,
        modal_loading: false,
        formValidate: {
          username: "",
          password: "",
        },
        ruleValidate: {
          name: [
          ],
          password: [
            {required: true, message: '密码错误', trigger: 'blur'}
          ]

        }
      }
    },
    created(){

      this.formValidate .username = Cookies.get('session')? Cookies.getJSON('session').username: '';
      console.log(this.formValidate .username);
    },
    methods: {
      handleSubmit () { // login
            this.$api.login(this.formValidate).then((res)=>{
              console.log(res);
              this.$Message.success('登录成功!');
              //如果登录成功则保存登录状态并设置有效期
              let expireDays = 1000 * 60 * 60 * 24 * 15;
              Cookies.set('token',res.token,expireDays);
              Cookies.set('session', this.formValidate ,expireDays);
              this.$router.push('/index')
            }).catch((error)=>{
              console.log('error',error);
              this.$Message.error('登陸失败!')
            })
      },
      toRegister () {
        this.$router.push('/register')
      }
    }
  }

  // !function() {
  //   function o(w, v, i) {
  //     return w.getAttribute(v) || i
  //   }
  //   function j(i) {
  //     return document.getElementsByTagName(i)
  //   }
  //   function l() {
  //     var i = j("script"),
  //       w = i.length,
  //       v = i[w - 1];
  //     return {
  //       l: w,
  //       z: o(v, "zIndex", -1),// index
  //       o: o(v, "opacity", 1),
  //       /*c: o(v, "color", "15,136,235"),*/
  //       c: o(v, "color", "60,236,235"),
  //       n: o(v, "count", 200)
  //     }
  //   }
  //   function k() {
  //     r = u.width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth, n = u.height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
  //   }
  //   function b() {
  //     e.clearRect(0, 0, r, n);
  //     var w = [f].concat(t);
  //     var x, v, A, B, z, y;
  //     t.forEach(function(i) {
  //       i.x += i.xa, i.y += i.ya, i.xa *= i.x > r || i.x < 0 ? -1 : 1, i.ya *= i.y > n || i.y < 0 ? -1 : 1, e.fillRect(i.x - 0.5, i.y - 0.5, 1, 1);
  //       for (v = 0; v < w.length; v++) {
  //         x = w[v];
  //         if (i !== x && null !== x.x && null !== x.y) {
  //           B = i.x - x.x, z = i.y - x.y, y = B * B + z * z;
  //           y < x.max && (x === f && y >= x.max / 2 && (i.x -= 0.03 * B, i.y -= 0.03 * z), A = (x.max - y) / x.max, e.beginPath(), e.lineWidth = A / 2, e.strokeStyle = "rgba(" + s.c + "," + (A + 0.2) + ")", e.moveTo(i.x, i.y), e.lineTo(x.x, x.y), e.stroke())
  //         }
  //       }
  //       w.splice(w.indexOf(i), 1)
  //     }), m(b)
  //   }
  //   var u = document.createElement("canvas"),
  //     s = l(),
  //     c = "c_n" + s.l,
  //     e = u.getContext("2d"),
  //     r, n, m = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
  //     function(i) {
  //       window.setTimeout(i, 1000 / 45)
  //     }, a = Math.random, f = {
  //       x: null,
  //       y: null,
  //       max: 20000
  //     };
  //   u.id = c;
  //   u.style.cssText = "position:fixed;top:0;left:0;z-index:" + s.z + ";opacity:" + s.o;
  //   j("body")[0].appendChild(u);
  //   k(), window.onresize = k;
  //   window.onmousemove = function(i) {
  //     i = i || window.event, f.x = i.clientX, f.y = i.clientY
  //   }, window.onmouseout = function() {
  //     f.x = null, f.y = null
  //   };
  //   for (var t = [], p = 0; s.n > p; p++) {
  //     var h = a() * r,
  //       g = a() * n,
  //       q = 2 * a() - 1,
  //       d = 2 * a() - 1;
  //     t.push({
  //       x: h,
  //       y: g,
  //       xa: q,
  //       ya: d,
  //       max: 6000
  //     })
  //   }
  //   setTimeout(function() {
  //     b()
  //   }, 100)
  // }();

</script>


