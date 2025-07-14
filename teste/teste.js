// Initial points in a triangle
const A = [0, 0]; // -> Fixo
let B = [0, 10]; // -> Variavel
let C = [10, 10]; // -> Variavel

const lawOfCosines = (a, b, c, angle, side) => {
  // convert degrees → radians
  const θ = angle * Math.PI / 180;

  switch (side.toLowerCase()) {
    case 'a':
      // a² = b² + c² − 2bc·cos(A)
      if (b == null || c == null) throw new Error("Need b and c to find a");
      return Math.sqrt(b * b + c * c - 2 * b * c * Math.cos(θ));

    case 'b':
      // b² = a² + c² − 2ac·cos(B)
      if (a == null || c == null) throw new Error("Need a and c to find b");
      return Math.sqrt(a * a + c * c - 2 * a * c * Math.cos(θ));

    case 'c':
      // c² = a² + b² − 2ab·cos(C)
      if (a == null || b == null) throw new Error("Need a and b to find c");
      return Math.sqrt(a * a + b * b - 2 * a * b * Math.cos(θ));

    default:
      throw new Error("`side` must be one of 'a', 'b', or 'c'");
  }
};

class Joint {
  // Colocar ang min e max tambem
  constructor(name, x, y, z = 0, angle, movel = true) {
    this.name = name
    this.x = x
    this.y = y
    this.z = z // Desativado eixo z no inicio
    this.angle = angle
    this.movel = movel

    // Outras configurações do arduino e servo irão aqui
  }

  getAngle() {
    return this.angle
  }

  coordinates() {
    return [this.x, this.y, this.z]
  }

  // Atualiza angulo do motor e recalcula e atualiza coordenadas no mapa se a junta for móvel no plano
  updateAngle(newAngle) {
    this.angle = newAngle
    if (this.movel) {
      // atualizar posicao no mapa
      // 
    }
  }

  updateCoordinates(x, y, z = this.z) {
    if (this.movel) {
      this.x = x;
      this.y = y;
      this.z = z;
    }
  }
}

const shoulder = new Joint("shoulder", 0, 0, 0, 45, false)
const elbow = new Joint("elbow", 0, 10, 0, 90)
const claw = new Joint("claw", 10, 10, 0, 45)

class RoboticArm {
  constructor(shoulderJoint, elbowJoint, clawJoint) {
    this.shoulderJoint = shoulderJoint;
    this.elbowJoint = elbowJoint;
    this.clawJoint = clawJoint;

    // Comprimentos fixos dos segmentos do braço
    this.segmentLength1 = 10; // Ombro para cotovelo
    this.segmentLength2 = 10; // Cotovelo para garra

    this.updateArmGeometry();
  }

  updateArmGeometry() {
    this.A = this.shoulderJoint.coordinates();
    this.B = this.elbowJoint.coordinates();
    this.C = this.clawJoint.coordinates();

    this.AB = [this.B[0] - this.A[0], this.B[1] - this.A[1]];
    this.BC = [this.C[0] - this.B[0], this.C[1] - this.B[1]];
    this.AC = [this.C[0] - this.A[0], this.C[1] - this.A[1]];

    this.moduloAB = Math.sqrt(this.AB[0] ** 2 + this.AB[1] ** 2);
    this.moduloBC = Math.sqrt(this.BC[0] ** 2 + this.BC[1] ** 2);
    this.moduloAC = Math.sqrt(this.AC[0] ** 2 + this.AC[1] ** 2);

    this.a = this.moduloBC; // Distância BC
    this.b = this.moduloAC; // Distância AC (distância da garra)
    this.c = this.moduloAB; // Distância AB
  }

  moveClawFront(distance) {
    console.log(`\nMovendo garra ${distance} unidades para frente...`);
    // Para mover para frente, deve-se alterar o valor da reta AC para o tamanho final do movimento
    // Exemplo: mover garra dois cm para frente é resultado da trigonometria para calcular os angulos nas `Joints` Shoulder e Elbow
    const newClawDistance = this.b + distance

    // Verificar se o movimento é possível
    const maxReach = this.segmentLength1 + this.segmentLength2;
    const minReach = Math.abs(this.segmentLength1 - this.segmentLength2);

    if (newClawDistance > maxReach || newClawDistance < minReach) {
      console.log(`Movimento impossível. Alcance deve estar entre ${minReach} e ${maxReach}`);
      return;
    }

    // Calcular novos ângulos usando lei dos cossenos
    // Para um braço de dois segmentos, calculamos os ângulos internos do triângulo
    // Calculo com lei dos cossenos para achar novos angulos -> Ver mais informacoes na documentacao
    // p = a √(2 - 2 cos(B))

    // Ângulo no cotovelo (interno)
    const cosElbowAngle = (this.segmentLength1 ** 2 + this.segmentLength2 ** 2 - newClawDistance ** 2) / 
                         (2 * this.segmentLength1 * this.segmentLength2);
    const elbowAngleRad = Math.acos(Math.max(-1, Math.min(1, cosElbowAngle)));
    
    // Ângulo no ombro (interno do triângulo)
    const cosShoulderAngle = (this.segmentLength1 ** 2 + newClawDistance ** 2 - this.segmentLength2 ** 2) / 
                            (2 * this.segmentLength1 * newClawDistance);
    const shoulderAngleRad = Math.acos(Math.max(-1, Math.min(1, cosShoulderAngle)));
    
    // Converter para graus
    const elbowAngleDegrees = elbowAngleRad * 180 / Math.PI;
    const shoulderAngleDegrees = shoulderAngleRad * 180 / Math.PI;
    
    console.log(`Novo ângulo do ombro: ${shoulderAngleDegrees.toFixed(2)}°`);
    console.log(`Novo ângulo do cotovelo: ${elbowAngleDegrees.toFixed(2)}°`);
    
    // Atualizar os ângulos das joints
    this.shoulderJoint.updateAngle(shoulderAngleDegrees);
    this.elbowJoint.updateAngle(elbowAngleDegrees);
    
    //* Calcular novas posições das joints

    // Cotovelo: posição baseada no ângulo do ombro
    // const elbowX = this.shoulderJoint.x + this.segmentLength1 * Math.cos(shoulderAngleRad);
    const elbowX = this.segmentLength1 * Math.cos(shoulderAngleRad);
    // const elbowY = this.shoulderJoint.y + this.segmentLength1 * Math.sin(shoulderAngleRad);
    const elbowY = this.segmentLength1 * Math.sin(shoulderAngleRad);
    
    // Garra: posição baseada na posição do cotovelo e ângulo do cotovelo
    const clawAngleFromHorizontal = shoulderAngleRad + (Math.PI - elbowAngleRad);
    const clawX = elbowX + this.segmentLength2 * Math.cos(clawAngleFromHorizontal);
    const clawY = elbowY + this.segmentLength2 * Math.sin(clawAngleFromHorizontal);
    
    // Atualizar coordenadas das joints móveis
    this.elbowJoint.updateCoordinates(elbowX, elbowY);
    this.clawJoint.updateCoordinates(clawX, clawY);
    
    // Atualizar geometria do braço
    this.updateArmGeometry();
    
    console.log(`Nova posição do cotovelo: (${elbowX.toFixed(2)}, ${elbowY.toFixed(2)})`);
    console.log(`Nova posição da garra: (${clawX.toFixed(2)}, ${clawY.toFixed(2)})`);
    console.log(`Nova distância da garra: ${this.b.toFixed(2)}`);
  }

  joints() {
    console.log("Shoulder:", this.A);
    console.log("Elbow:", this.B);
    console.log("Claw:", this.C);
  }

  parts() {
    console.log("Length a:", this.a);
    console.log("Length b:", this.b);
    console.log("Length c:", this.c);
  }

  angles() {
    console.log("Angle A:", this.angleA);
    console.log("Angle B:", this.angleB);
    console.log("Angle C:", this.angleC);
  }
}

const arm1 = new RoboticArm(shoulder, elbow, claw)
arm1.joints()
arm1.parts()

setTimeout(() => {
  console.log("\nNovos dados:\n");
  arm1.moveClawFront(1.0)

  arm1.joints()
  arm1.parts()
}, 1500);