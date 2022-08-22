from matplotlib import pyplot as plt


def plt_meth(imagen_salida, imagen=None):
    """
    Esta funcion bvlalbalbabla
    :param
        -imagen_salida(ImageBuffer): resultado
        -image(ImageBuffer): imagen en bruto
    """

    plt.figure(figsize=[15, 15])
    plt.subplot(121)
    if imagen:
        plt.imshow(imagen[:, :, ::-1])
        plt.title("Imagen Original")

    plt.axis('off')
    plt.subplot(122)
    plt.imshow(imagen_salida[:, :, ::-1])
    plt.title("Salida")
    plt.axis('off')
