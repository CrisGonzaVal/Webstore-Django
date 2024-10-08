

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id_categoria', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('edad', models.IntegerField()),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('dv', models.CharField(max_length=1)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TipoPago',
            fields=[
                ('id_n_tarjeta', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('banco', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Despacho',
            fields=[
                ('id_despacho', models.AutoField(primary_key=True, serialize=False)),
                ('estatus', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_prod', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('valor', models.IntegerField(default=0)),
                ('color', models.CharField(max_length=50)),
                ('imagen', models.ImageField(null=True, upload_to='producto')),
                ('id_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Fecha',
            fields=[
                ('id_fecha', models.AutoField(primary_key=True, serialize=False)),
                ('anio', models.IntegerField()),
                ('mes', models.IntegerField()),
                ('dia', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Importadora',
            fields=[
                ('rut_empresa', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id_marca', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_m', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedores',
            fields=[
                ('id_proveedor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TipoUsuario',
            fields=[
                ('id_tipo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.usuario')),
                ('rol', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_comuna', models.CharField(max_length=100)),
                ('id_ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ciudad')),
            ],
        ),
        migrations.CreateModel(
            name='Credito',
            fields=[
                ('id_n_tarjeta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.tipopago')),
            ],
        ),
        migrations.CreateModel(
            name='Debito',
            fields=[
                ('id_n_tarjeta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.tipopago')),
            ],
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id_cuenta', models.AutoField(primary_key=True, serialize=False)),
                ('clave_usuario', models.CharField(max_length=100)),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Dimensiones',
            fields=[
                ('id_producto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.producto')),
                ('alto', models.FloatField()),
                ('largo', models.FloatField()),
                ('ancho', models.FloatField()),
                ('peso', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id_producto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.producto')),
                ('cantidad', models.IntegerField()),
                ('ubicacion', models.CharField(max_length=100)),
                ('estatus', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=50)),
                ('calle', models.CharField(max_length=100)),
                ('numero', models.IntegerField()),
                ('id_despacho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.despacho')),
            ],
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id_registro', models.AutoField(primary_key=True, serialize=False)),
                ('accion', models.TextField()),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id_bodega', models.AutoField(primary_key=True, serialize=False)),
                ('rut_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.importadora')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='id_marca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.marca'),
        ),
        migrations.CreateModel(
            name='OrdenCompra',
            fields=[
                ('id_orden_compra', models.AutoField(primary_key=True, serialize=False)),
                ('id_proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.proveedores')),
            ],
        ),
        migrations.AddField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tipousuario'),
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id_venta', models.AutoField(primary_key=True, serialize=False)),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producto')),
            ],
        ),
        migrations.AddField(
            model_name='despacho',
            name='id_venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.venta'),
        ),
        migrations.CreateModel(
            name='ComprobantePago',
            fields=[
                ('id_comprobante', models.AutoField(primary_key=True, serialize=False)),
                ('id_venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.venta')),
            ],
        ),
    ]
