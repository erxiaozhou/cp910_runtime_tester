(module
  (type (;0;) (func (param i32 i32 i32 i32) (result i32)))
  (type (;1;) (func (param i32)))
  (type (;2;) (func))
  (type (;3;) (func (result f32)))
  (func (;0;) (type 3) (result f32)
    (local i32 f32 i64 f64)
    i32.const 305419896
    local.set 0
    f32.const 0x1.8cp+6 (;=99;)
    local.set 1
    i64.const -72057589709208571
    local.set 2
    f64.const 0x1.5f0b08c960a79p+109 (;=8.9e+32;)
    local.set 3
    f32.const -0x1.3221d4p+125 (;=-5.08649e+37;)
    f32.abs
    local.get 0
    global.set 8
    local.get 1
    global.set 9
    local.get 2
    global.set 10
    local.get 3
    global.set 11)
  (memory (;0;) 1)
  (global (;0;) i32 (i32.const 541))
  (global (;1;) (mut i32) (i32.const 191))
  (global (;2;) f32 (f32.const 0x1.0e8p+9 (;=541;)))
  (global (;3;) (mut f32) (f32.const 0x1.8p+7 (;=192;)))
  (global (;4;) i64 (i64.const 54))
  (global (;5;) (mut i64) (i64.const 19))
  (global (;6;) f64 (f64.const 0x1.bp+5 (;=54;)))
  (global (;7;) (mut f64) (f64.const 0x1.3p+4 (;=19;)))
  (global (;8;) (mut i32) (i32.const 0))
  (global (;9;) (mut f32) (f32.const 0x0p+0 (;=0;)))
  (global (;10;) (mut i64) (i64.const 0))
  (global (;11;) (mut f64) (f64.const 0x0p+0 (;=0;)))
  (export "_start" (func 0))
  (export "to_test" (func 0))
  (data (;0;) (i32.const 8) "\10\00\00\00\0d\00\00\00")
  (data (;1;) (i32.const 16) "Hello World!\0a")
  (data (;2;) (i32.const 32) "Hello World!\0a"))
