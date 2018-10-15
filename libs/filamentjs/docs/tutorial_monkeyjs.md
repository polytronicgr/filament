<iframe style="width:100%;height:200px;border:none" src="demo_monkeyjs.html"></iframe>

```js {fragment="root"}
class App {
  constructor() {

    this.canvas = document.getElementsByTagName('canvas')[0]
    const engine = this.engine = Filament.Engine.create(this.canvas);
    this.scene = engine.createScene();

    this.monkey = Filament.EntityManager.get() .create();
    this.scene.addEntity(this.monkey);

    const TRIANGLE_POSITIONS = Filament.Buffer(new Float32Array([
      1, 0,
      Math.cos(Math.PI * 2 / 3), Math.sin(Math.PI * 2 / 3),
      Math.cos(Math.PI * 4 / 3), Math.sin(Math.PI * 4 / 3),
    ]));
    const TRIANGLE_COLORS = Filament.Buffer(new Uint32Array([
      0xffff0000,
      0xff00ff00,
      0xff0000ff,
    ]));
    const TEXTURED_LIT_PACKAGE = Filament.Buffer(Filament.assets['texturedLit.filamat']);
    const FILAMESH = Filament.Buffer(Filament.assets['monkey.filamesh']);

    const VertexAttribute = Filament.VertexAttribute;
    const AttributeType = Filament.VertexBuffer$AttributeType;
    this.vb = Filament.VertexBuffer.Builder()
      .vertexCount(3)
      .bufferCount(2)
      .attribute(VertexAttribute.POSITION, 0, AttributeType.FLOAT2, 0, 8)
      .attribute(VertexAttribute.COLOR, 1, AttributeType.UBYTE4, 0, 4)
      .normalized(VertexAttribute.COLOR)
      .build(engine);
    this.vb.setBufferAt(engine, 0, TRIANGLE_POSITIONS);
    this.vb.setBufferAt(engine, 1, TRIANGLE_COLORS);
    this.ib = Filament.IndexBuffer.Builder()
      .indexCount(3)
      .bufferType(Filament.IndexBuffer$IndexType.USHORT)
      .build(engine);
    this.ib.setBuffer(engine, Filament.Buffer(new Uint16Array([0, 1, 2])));

    const mat = engine.createMaterial(TEXTURED_LIT_PACKAGE);
    const matinst = mat.getDefaultInstance();
    Filament.RenderableManager.Builder(1)
      .boundingBox([
        [-1, -1, -1],
        [1, 1, 1]
      ])
      .material(0, matinst)
      .geometry(0, Filament.RenderableManager$PrimitiveType.TRIANGLES, this.vb, this.ib)
      .build(engine, this.monkey);

    this.swapChain = engine.createSwapChain();
    this.renderer = engine.createRenderer();
    this.camera = engine.createCamera();
    this.view = engine.createView();
    this.view.setCamera(this.camera);
    this.view.setClearColor([.5, .5, .5, .5]);
    this.view.setScene(this.scene);
    this.resize();
    this.render = this.render.bind(this);
    this.resize = this.resize.bind(this);
    window.addEventListener("resize", this.resize);
    window.requestAnimationFrame(this.render);
  }
  render() {
    if (this.renderer.beginFrame(this.swapChain)) {
      this.renderer.render(this.view);
      this.renderer.endFrame();
    }
    this.engine.execute();
    window.requestAnimationFrame(this.render);
  }
  resize() {
    const dpr = window.devicePixelRatio;
    const width = this.canvas.width = window.innerWidth * dpr;
    const height = this.canvas.height = window.innerHeight * dpr;
    this.view.setViewport([0, 0, width, height]);
    const aspect = width / height;
    const Projection = Filament.Camera$Projection;
    this.camera.setProjection(Projection.ORTHO, -aspect, aspect, -1, 1, 0, 1);
  }
}
Filament.init(['texturedLit.filamat', 'monkey.filamesh'], () => {
  Window.app = new App()
});
```
